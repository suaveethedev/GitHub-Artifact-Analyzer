# GitHub Artifact Analyzer

This Python script is inspired by the article [GitHub Attack Vector Cracks Open Google, Microsoft, AWS Projects.](https://www.darkreading.com/cloud-security/github-attack-vector-google-microsoft-aws-projects)
The script is designed to analyze GitHub repository build artifacts for potential leaks of sensitive information.

### Features
* Download Artifacts: Fetches build artifacts from a specified GitHub repository.
* Sensitive Data Scanning: Analyzes log files in the artifacts for potential sensitive information.
* Output: Displays any potential sensitive information found directly in the terminal.

### Usage
```zsh
foo@bar build_artifact_search % chmod +x github_artifact_analyzer.py
foo@bar build_artifact_search % ./github_artifact_analyzer.py <owner>/<repo_name> <github_token>
```
### Arguments
* \<owner>/\<repo>: The GitHub repository to analyze
* \<token>: Your [GitHub token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with the necessary permissions

### Example
```zsh
foo@bar build_artifact_search % ./github_artifact_analyzer.py username/my-repo ghp_1234567890abcdefghijklmnopqrstu
```

### How It Works
1. **Artifact Download:** The script downloads all build artifacts from the specified GitHub repository and saves them into a local folder named after the project.
2. **Sensitive Data Search:** It then searches through the log files in the artifacts for common sensitive strings such as:
   * AWS Access Keys
   * API Tokens
   * Passwords
   * Database URLs
   * Other environment variables
3. **Output:** The results are outputted directly to the terminal, indicating potential leaks

### Future Enhancements
* Add support for more file types.
* Improve pattern recognition for sensitive data.
* Option to output results to a file or send alerts

### Contributing
Feel free to open issues or submit pull requests if you have suggestions for improvements or new features.
