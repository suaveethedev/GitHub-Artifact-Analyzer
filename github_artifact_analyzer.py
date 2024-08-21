#!/usr/bin/env python3
import argparse, os, re, requests, zipfile
from utils.repo_utils import get_repos_for_owner
from utils.file_utils import search_files_for_sensitive_info, extract_zip_files_from_folder
from utils.artifact_utils import download_artifacts_concurrently


def main():
    parser = argparse.ArgumentParser(
        description='Script to download GitHub artifacts and search for sensitive information.')

    # Required GitHub token argument
    parser.add_argument("--token", "-t", required=True, help="GitHub token is required for authentication.")

    # optional user and repo arguments
    parser.add_argument( "--user", "-u", help="GitHub username or organization name.", type=str)
    parser.add_argument( "--repo", "-r",
                         help="GitHub repository name (optional, but must be used with --user).", type=str)
    parser.add_argument("--output", "-o",
                        help="Filepath to store the secrets extracted from artifacts.", type=str)

    args = parser.parse_args()

    # Ensure either --user or both --user and --repo are provided along with the token
    if not args.user and not args.repo:
        parser.error("You must provide either a --user or a --user with --repo along with the --token.")

    # If --repo is provided, --user must be provided as well
    if args.repo and not args.user:
        parser.error("--repo requires --user to be specified.")

    # Arguments passed successfully, proceed with the script logic
    artifact_folder = os.path.join(os.getcwd() + "artifacts")
    if args.user and args.repo:
        print(f"Owner/Repo: {args.user}/{args.repo}")

        # Folders to use in later programming
        working_folder = os.getcwd() + "/{}".format(args.repo)
        zipped_folder = working_folder + "/zipped"
        log_folder = working_folder + "/logs"
        os.makedirs(zipped_folder, exist_ok=True)
        os.makedirs(log_folder, exist_ok=True)

        # GitHub Actions Artifacts API URL
        artifacts_url = f"https://api.github.com/repos/{args.user}/{args.repo}/actions/artifacts"

        # Headers for the API request
        headers = {
            "Authorization": f"token {args.token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Make a request to the GitHub Actions API to get the list of artifacts
        response = requests.get(artifacts_url, headers=headers)
        artifacts = response.json()  # Response to iterate and pass to function

        download_artifacts_concurrently(artifacts, zipped_folder, args.user, args.repo, headers)

        # Issue is the root directory contains a folder
        extract_zip_files_from_folder(zipped_folder, log_folder)

        # Setting the file path for the file containing the sensitive data
        if args.output:
            output_file = args.output
        else:
            output_file = os.path.join(working_folder, "secrets.txt")

        search_files_for_sensitive_info(log_folder, output_file)

    elif args.user:
        print(f"User/Owner: {args.user}")
        repos = get_repos_for_owner(args.token, args.user)
        for repo in repos:

            # Folders to use in later programming
            working_folder = os.getcwd() + "/artifacts/{}".format(repo)
            zipped_folder = os.path.join(working_folder, "zipped")
            log_folder = working_folder + "/logs"

            os.makedirs(zipped_folder, exist_ok=True)
            os.makedirs(log_folder, exist_ok=True)
            os.makedirs(working_folder + "/secrets")

            # GitHub Actions Artifacts API URL
            artifacts_url = f"https://api.github.com/repos/{args.user}/{repo}/actions/artifacts"

            # Headers for the API request
            headers = {
                "Authorization": f"token {args.token}",
                "Accept": "application/vnd.github.v3+json"
            }

            # Make a request to the GitHub Actions API to get the list of artifacts
            response = requests.get(artifacts_url, headers=headers)
            artifacts = response.json()  # Response to iterate and pass to

            download_artifacts_concurrently(artifacts, zipped_folder, args.user, repo, headers)

            # Issue is the root directory contains a folder
            extract_zip_files_from_folder(zipped_folder, log_folder)

            # Setting the file path for the file containing the sensitive data

            output_file = os.path.join(working_folder, f"secrets/{repo}.txt")
            print("Output file path: ", output_file)
            search_files_for_sensitive_info(log_folder, output_file)


if __name__ == "__main__":
    main()
