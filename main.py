import os
import shutil
import subprocess
import time

import requests
from dotenv import load_dotenv

load_dotenv()

github_username = os.environ.get('GITHUB_USERNAME')
github_token = os.environ.get('GITHUB_TOKEN')
clone_dir = os.environ.get('CLONE_DIR')

url = f'https://api.github.com/user/repos'
params = {
    'per_page': 100,
    'page': 1,
    'type': 'owner',
}
headers = {'Authorization': f'token {github_token}'}

repos = []

# Fetch all repositories (handle pagination)
while True:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        break
    repos.extend(data)
    params['page'] += 1

print(f"Found {len(repos)} repositories.")

# Auto clean up the clone directory before cloning
if os.path.exists(clone_dir):
    shutil.rmtree(clone_dir)
os.makedirs(clone_dir, exist_ok=True)

time.sleep(1)

# Clone each repository
for repo in repos:
    clone_url = repo['clone_url']
    repo_name = repo['name']
    dest_path = os.path.join(clone_dir, repo_name)
    subprocess.run(['git', 'clone', clone_url, dest_path])

print("All repositories cloned.")