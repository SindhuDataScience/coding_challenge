import requests

# workspace = 'atlassian'  # Replace with the public workspace ID you want to query
#
# url = f'https://api.bitbucket.org/2.0/repositories/mailchimp'
#
# response = requests.get(url)
#
# if response.status_code == 200:
#     data = response.json()
#     for repo in data['values']:
#         print(f"{repo['name']} - {repo['links']['html']['href']}")
# else:
#     print(f"Error: {response.status_code} - {response.text}")
team_name='mailchimp'
repos_url = f'https://api.bitbucket.org/2.0/repositories/{team_name}'
repos_response = requests.get(repos_url)
# repos_url = f'https://api.bitbucket.org/2.0/teams/{team_name}/repositories'
# repos_response = requests.get(repos_url, headers=bitbucket_headers)

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

print(data)
