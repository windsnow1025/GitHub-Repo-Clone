import asyncio
import os
import stat
import shutil
import subprocess

import httpx
from dotenv import load_dotenv


def rmtree_readonly(path):
    def on_error(_func, fpath, _exc_info):
        os.chmod(fpath, stat.S_IWRITE)
        os.unlink(fpath)

    shutil.rmtree(path, onexc=on_error)


async def main():
    load_dotenv()

    github_token = os.environ.get('GITHUB_TOKEN')
    clone_dir = os.environ.get('CLONE_DIR')
    temp_dir = os.environ.get('TEMP_DIR')

    url = 'https://api.github.com/user/repos'
    params = {
        'per_page': 100,
        'page': 1,
        'type': 'owner',
    }
    headers = {'Authorization': f'token {github_token}'}

    repos = []

    # Fetch all repositories
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            repos.extend(data)
            params['page'] += 1

    print(f"Found {len(repos)} repositories.")

    # Clone to local temp directory to avoid Google Drive interference
    if os.path.exists(temp_dir):
        rmtree_readonly(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    await asyncio.sleep(1)

    for repo in repos:
        clone_url = repo['clone_url']
        repo_name = repo['name']
        dest_path = os.path.join(temp_dir, repo_name)
        subprocess.run(['git', 'clone', clone_url, dest_path], check=True)

    print("All repositories cloned. Moving to target directory...")

    # Move cloned repos to target directory
    if os.path.exists(clone_dir):
        rmtree_readonly(clone_dir)
    os.makedirs(clone_dir, exist_ok=True)

    for repo in repos:
        repo_name = repo['name']
        src = os.path.join(temp_dir, repo_name)
        dst = os.path.join(clone_dir, repo_name)
        print(f"Copying {repo_name}...")
        shutil.copytree(src, dst)

    rmtree_readonly(temp_dir)

    print("All repositories moved to target directory.")


asyncio.run(main())
