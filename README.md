GitHub Artifact Analyzer

This Python script is inspired by the article "GitHub Attack Vector Cracks Open Google, Microsoft, AWS Projects."
The script is designed to analyze GitHub repository build artifacts for potential leaks of sensitive information.

Features

*Download Artifacts: Fetches build artifacts from a specified GitHub repository.

*Sensitive Data Scanning: Analyzes log files in the artifacts for potential sensitive information.

*Output: Displays any potential sensitive information found directly in the terminal.

Usage
```zsh
foo@bar build_artifact_search % ./github_artifact_analyzer.py <owner>/<repo_name> <github_token>
```