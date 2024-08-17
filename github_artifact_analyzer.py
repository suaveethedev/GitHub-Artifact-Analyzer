#!/usr/bin/env python3
import argparse, os, re, requests, zipfile

parser = argparse.ArgumentParser(description='Used to search through a folder containing build artifacts')
parser.add_argument("repo", help="<owner>/<repo>")
parser.add_argument("token", help="github token to authenticate to github")
# parser.add_argument('folder', help='folder containing log files', nargs='*')
args = parser.parse_args()

patterns = [
    r'AWS_ACCESS_KEY_ID\s*=\s*[\'"]?([A-Z0-9]{20})[\'"]?',
    r'AWS_SECRET_ACCESS_KEY\s*=\s*[\'"]?([A-Za-z0-9/+=]{40})[\'"]?',
    r'GCP_SERVICE_ACCOUNT_KEY\s*=\s*[\'"]?([A-Za-z0-9-]{30,})[\'"]?',
    r'AZURE_CLIENT_ID\s*=\s*[\'"]?([a-z0-9-]{36})[\'"]?',
    r'AZURE_CLIENT_SECRET\s*=\s*[\'"]?([a-zA-Z0-9-_]{32,})[\'"]?',
    r'DB_PASSWORD\s*=\s*[\'"]?(.+)[\'"]?',
    r'DATABASE_URL\s*=\s*[\'"]?(.+)[\'"]?',
    r'API_KEY\s*=\s*[\'"]?(.+)[\'"]?',
    r'SECRET_KEY\s*=\s*[\'"]?(.+)[\'"]?',
    r'JWT_SECRET\s*=\s*[\'"]?(.+)[\'"]?',
    r'SSH_PRIVATE_KEY\s*=\s*[\'"]?(.+)[\'"]?',
    r'GITHUB_TOKEN\s*=\s*[\'"]?(.+)[\'"]?',
    r'CI_JOB_TOKEN\s*=\s*[\'"]?(.+)[\'"]?',
    r'SLACK_WEBHOOK_URL\s*=\s*[\'"]?(.+)[\'"]?',
    r'Authorization:\s*[\'"]?(.+)[\'"]?',
    r'Bearer\s+([A-Za-z0-9-_\.]+)',
    r'client_secret\s*=\s*[\'"]?(.+)[\'"]?',
    r'client_id\s*=\s*[\'"]?(.+)[\'"]?',
    r'.pem\s*=\s*[\'"]?(.+)[\'"]?',
    r'.key\s*=\s*[\'"]?(.+)[\'"]?',
    r'password\s*=\s*[\'"]?(.+)[\'"]?',
    r'arn:(aws|aws-us-gov|aws-cn):'
]
combined_pattern = re.compile('|'.join(patterns))
owner, repo_name = str(args.repo).split("/")

# GitHub Actions Artifacts API URL
artifacts_url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/artifacts"

# Headers for the API request
headers = {
    "Authorization": f"token {args.token}",
    "Accept": "application/vnd.github.v3+json"
}

# Make a request to the GitHub Actions API to get the list of artifacts
response = requests.get(artifacts_url, headers=headers)
artifacts = response.json()

working_folder = os.getcwd() + "/{}".format(repo_name)
zipped_folder = working_folder + "/zipped"
log_folder = working_folder + "/logs"

os.makedirs(zipped_folder, exist_ok=True)
os.makedirs(log_folder, exist_ok=True)

for artifact in artifacts.get("artifacts", []):
    artifact_id = artifact["id"]
    artifact_name = artifact["name"]

    file_path = os.path.join(zipped_folder, f"{artifact_id}.zip")
    if not os.path.exists(file_path):
        # URL to download the artifact
        download_url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/artifacts/{artifact_id}/zip"

        # Download the artifact
        download_response = requests.get(download_url, headers=headers)

        print(f"writing {artifact_id}.zip")
        with open(file_path, "wb") as f:
            f.write(download_response.content)
            f.close()
    else:
        print(f"{artifact_id}.zip already exists .. skipping")

# Issue is the root directory contains a folder
for filename in os.listdir(zipped_folder):
    file_path = os.path.join(zipped_folder, f"{filename}")
    if os.path.isfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(f"{log_folder}")
            zip_ref.close()

for file in os.listdir(f"{log_folder}"):
    with open(f"{log_folder}/{file}", "r") as open_file:
        try:
            for i, line in enumerate(open_file.readlines(), start=1):
                match = combined_pattern.search(line)
                if match:
                    print(f"Potential secret found in {working_folder}/artifacts_contents/{file} on line {i}:")
                    print(f"\tMatched string: {line.strip()}")
            open_file.close()
        except UnicodeDecodeError:
            print(f"File: {file} is not un utf-8.")
