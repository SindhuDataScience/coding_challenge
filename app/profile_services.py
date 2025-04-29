import requests
import logging

logger = logging.getLogger(__name__)

def get_github_data(github_headers, org_name):
    """Fetch GitHub organization data using requests."""
    try:
        # Get organization details
        org_url = f'https://api.github.com/orgs/{org_name}'
        org_response = requests.get(org_url, headers=github_headers)
        if org_response.status_code != 200:
            logger.error(f"GitHub API error: {org_response.status_code} - {org_response.text}")
            return None
        org_data = org_response.json()

        # Get repositories
        repos_url = f'https://api.github.com/orgs/{org_name}/repos'
        repos_response = requests.get(repos_url, headers=github_headers)
        if repos_response.status_code != 200:
            logger.error(f"GitHub API error: {repos_response.status_code} - {repos_response.text}")
            return None
        repos = repos_response.json()

        data = {
            'public_repos': 0,
            'forked_repos': 0,
            'watchers': org_data.get('watchers', 0),
            'languages': {},
            'topics': {}
        }

        for repo in repos:
            if not repo.get('private'):
                data['public_repos'] += 1
            if repo.get('fork'):
                data['forked_repos'] += 1
            # Get languages
            langs_url = repo.get('languages_url')
            langs_response = requests.get(langs_url, headers=github_headers)
            if langs_response.status_code == 200:
                langs = langs_response.json()
                for lang, bytes_count in langs.items():
                    data['languages'][lang] = data['languages'].get(lang, 0) + bytes_count
            # Get topics
            topics = repo.get('topics', [])
            for topic in topics:
                data['topics'][topic] = data['topics'].get(topic, 0) + 1

        return data
    except Exception as e:
        logger.error(f"GitHub API error: {str(e)}")
        return None

def get_bitbucket_data(bitbucket_headers, team_name):
    """Fetch Bitbucket team data using requests."""
    try:

        # Get repositories
        repos_url = f'https://api.bitbucket.org/2.0/repositories/{team_name}'
        repos_response = requests.get(repos_url)
        if repos_response.status_code != 200:
            logger.error(f"Bitbucket API error: {repos_response.status_code} - {repos_response.text}")
            return None
        repos_data = repos_response.json()
        repos = repos_data.get('values', [])

        data = {
            'public_repos': 0,
            'forked_repos': 0,
            'watchers': 0,
            'languages': {},
            'topics': {}
        }

        for repo in repos:
            if not repo.get('is_private', True):
                data['public_repos'] += 1
                lang = repo.get('language', '')
                if lang:
                    data['languages'][lang] = data['languages'].get(lang, 0) + 1

        return data
    except Exception as e:
        logger.error(f"Bitbucket API error: {str(e)}")
        return None

def merge_data(github_data, bitbucket_data):
    """Merge data from both sources."""
    merged = {
        'total_public_repos': 0,
        'total_forked_repos': 0,
        'total_watchers': 0,
        'languages': {},
        'topics': {}
    }

    for data in [github_data, bitbucket_data]:
        if data:
            merged['total_public_repos'] += data['public_repos']
            merged['total_forked_repos'] += data['forked_repos']
            merged['total_watchers'] += data['watchers']
            for lang, count in data['languages'].items():
                merged['languages'][lang] = merged['languages'].get(lang, 0) + count
            for topic, count in data['topics'].items():
                merged['topics'][topic] = merged['topics'].get(topic, 0) + count

    return merged

def get_profiles(github_org, bitbucket_team):
    """
    Get merged organization profile from GitHub and Bitbucket.

    Args:
        github_org (str): GitHub organization name
        bitbucket_team (str): Bitbucket team name

    Returns:
        dict: Merged profile data and source status
    """
    github_headers = github_headers = {'Accept': 'application/vnd.github.v3+json'}
    bitbucket_headers = None

    github_data = get_github_data(github_headers, github_org)
    bitbucket_data = get_bitbucket_data(bitbucket_headers, bitbucket_team)

    # if not github_data and not bitbucket_data:
    #     raise Exception("Failed to fetch data")

    merged_data = merge_data(github_data, bitbucket_data)

    return {
        'data': merged_data,
        'sources': {
            'github': github_data is not None,
            'bitbucket': bitbucket_data is not None
        }
    }
