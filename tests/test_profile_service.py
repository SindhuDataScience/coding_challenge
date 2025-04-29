import pytest
import requests
import requests_mock
from app.profile_services import init_clients, get_github_data, get_bitbucket_data, merge_data, get_profiles

def test_init_clients_with_credentials():
    """Test init_clients with valid GitHub token and Bitbucket credentials."""
    github_token = "gh_token"
    bitbucket_username = "user"
    bitbucket_password = "pass"

    github_headers, bitbucket_headers = init_clients(github_token, bitbucket_username, bitbucket_password)

    assert github_headers == {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token gh_token'
    }
    assert bitbucket_headers == {
        'Accept': 'application/json',
        'Authorization': 'Basic dXNlcjpwYXNz'
    }

def test_get_github_data_success(requests_mock):
    """Test get_github_data with successful API responses."""
    org_name = "mailchimp"
    github_headers = {'Accept': 'application/vnd.github.v3+json'}

    # Mock organization response
    requests_mock.get(
        'https://api.github.com/orgs/mailchimp',
        json={'watchers': 100},
        status_code=200
    )

    # Mock repositories response
    requests_mock.get(
        'https://api.github.com/orgs/mailchimp/repos',
        json=[
            {'private': False, 'fork': False, 'languages_url': 'https://api.github.com/repos/mailchimp/repo1/languages', 'topics': ['api']}
        ],
        status_code=200
    )

    # Mock languages response
    requests_mock.get(
        'https://api.github.com/repos/mailchimp/repo1/languages',
        json={'Python': 1000},
        status_code=200
    )

    data = get_github_data(github_headers, org_name)

    assert data == {
        'public_repos': 1,
        'forked_repos': 0,
        'watchers': 100,
        'languages': {'Python': 1000},
        'topics': {'api': 1}
    }

def test_get_bitbucket_data_401(requests_mock):
    """Test get_bitbucket_data with 401 error."""
    team_name = "mailchimp"
    bitbucket_headers = {'Accept': 'application/json', 'Authorization': 'Basic dXNlcjpwYXNz'}

    requests_mock.get(
        f'https://api.bitbucket.org/2.0/teams/{team_name}/repositories',
        status_code=401,
        json={'error': 'Unauthorized'}
    )

    data = get_bitbucket_data(bitbucket_headers, team_name)

    assert data is None

def test_get_profiles_success(requests_mock):
    """Test get_profiles with successful API responses."""
    github_org = "mailchimp"
    bitbucket_team = "mailchimp"
    github_token = "gh_token"
    bitbucket_username = "user"
    bitbucket_password = "pass"

    # Mock GitHub responses
    requests_mock.get(
        'https://api.github.com/orgs/mailchimp',
        json={'watchers': 100},
        status_code=200
    )
    requests_mock.get(
        'https://api.github.com/orgs/mailchimp/repos',
        json=[{'private': False, 'fork': False, 'languages_url': 'https://api.github.com/repos/mailchimp/repo1/languages', 'topics': ['api']}],
        status_code=200
    )
    requests_mock.get(
        'https://api.github.com/repos/mailchimp/repo1/languages',
        json={'Python': 1000},
        status_code=200
    )

    # Mock Bitbucket response
    requests_mock.get(
        'https://api.bitbucket.org/2.0/teams/mailchimp/repositories',
        json={'values': [{'is_private': False, 'language': 'JavaScript', 'name': 'repo2'}]},
        status_code=200
    )

    result = get_profiles(github_org, bitbucket_team, github_token, bitbucket_username, bitbucket_password)

    assert result == {
        'data': {
            'total_public_repos': 2,
            'total_forked_repos': 0,
            'total_watchers': 100,
            'languages': {'Python': 1000, 'JavaScript': 1},
            'topics': {'api': 1}
        },
        'sources': {
            'github': True,
            'bitbucket': True
        }
    }
