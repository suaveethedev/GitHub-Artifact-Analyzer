from github import Github


def get_repos_for_owner(token: str, owner_name: str):
    """
        Fetch all repositories for the given user or organization.

        Args:
        - token (str): GitHub token for authentication.
        - owner_name (str): The GitHub username or organization name.

        Returns:
        - list: A list of repository full names (e.g., 'owner/repo_name').
        """
    g = Github(token)

    try:
        # Attempt to get the user or organization
        user_or_org = g.get_user(owner_name)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Fetch all repositories for the user or organization
    repos = user_or_org.get_repos()

    return [repo.name for repo in repos]  # or use repo.name if you want just the repo name
