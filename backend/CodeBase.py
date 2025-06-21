import requests
import os

token = os.getenv("GITHUB_TOKEN")
owner = 'jhthirteen'
repository = 'googleCalendarAssignments'

url = f'https://api.github.com/repos/{owner}/{repository}/contents'
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(url, headers=headers)

if( response.status_code != 200 ):
    print('Error: Failed to fetch repository contents, please try again')
    exit()

data = response.json()
file_names = []
for d in data:
    file_names.append(d['name'])

print(file_names)