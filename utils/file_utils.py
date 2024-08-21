import os
import re
import zipfile


def search_files_for_sensitive_info(log_folder_path, output_file_path):
    """
    Search for sensitive information in files within a folder.

    Args:
    - log_folder_path (str): Path to the folder containing files.
    - output_file_path (str): Path to the file holding sensitive output data.
    """
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

    for file in os.listdir(f"{log_folder_path}"):
        current_item = f"{log_folder_path}/{file}"

        if os.path.isfile(current_item):
            with open(current_item, "r") as open_file:
                try:
                    for i, line in enumerate(open_file.readlines(), start=1):
                        for word in line.split():
                            match = combined_pattern.search(word)
                            if match:
                                print(f"Potential secret found in {log_folder_path}/{file} on line {i}:")
                                print(f"\tMatched string: {word}")
                                if output_file_path is not None:
                                    with open(output_file_path, "a+") as output_file:
                                        if word not in output_file.readlines():
                                            output_file.write(word + "\n")
                                        output_file.close()  # Write to the output file
                except UnicodeDecodeError:
                    print(f"File: {file} is not un utf-8.")
        else:
            print(f"{current_item} is a directory .. skipping")


def extract_zip_files_from_folder(zipped_folder, log_folder):
    """
    Extracts all zip files from the specified folder and handles errors for corrupt zip files.

    Args:
        zipped_folder (str): Path to the folder containing zip files to be extracted.
        log_folder (str): Path to the folder where the extracted files will be saved.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified zipped_folder does not exist.
        PermissionError: If there are permission issues accessing the zipped_folder or log_folder.

    This function iterates over all files in the zipped_folder directory. For each file, it checks if it is a zip file
    and attempts to extract it to the log_folder. If a file is not a valid zip file or is corrupt, the function prints
    a message indicating the issue and skips that file.

    Example:
        >>> extract_zip_files_from_folder('/path/to/zipped_folder', '/path/to/log_folder')
    """
    for filename in os.listdir(zipped_folder):
        file_path = os.path.join(zipped_folder, f"{filename}")
        if os.path.isfile(file_path):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(f"{log_folder}")
            except zipfile.BadZipfile:
                print(f"{file_path} is a bad file path .. skipping")