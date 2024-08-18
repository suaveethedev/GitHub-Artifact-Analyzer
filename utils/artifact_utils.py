import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def _download_artifact(artifact, zip_folder, owner, repo_name, headers):
    artifact_id = artifact["id"]
    artifact_name = artifact["name"]
    file_path = os.path.join(zip_folder, f"{artifact_id}.zip")

    if not os.path.exists(file_path):
        # URL to download the artifact
        download_url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/artifacts/{artifact_id}/zip"

        try:
            # Download the artifact
            download_response = requests.get(download_url, headers=headers)
            download_response.raise_for_status()

            # Write the downloaded content to a file
            with open(file_path, 'wb') as file:
                file.write(download_response.content)
                file.close()
            print(f"Downloaded {artifact_name} to {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {artifact_name}: {e}")


def download_artifacts_concurrently(artifacts: dict, zip_folder, owner: str, repo_name: str, headers: dict,
                                    max_workers: int = 5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_download_artifact, artifact, zip_folder, owner, repo_name, headers)
            for artifact in artifacts.get("artifacts", [])
        ]

        # Optional: Process results as they complete
        for future in as_completed(futures):
            future.result()
