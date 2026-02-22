import asyncio
import os
import stat
import shutil
import subprocess

from dotenv import load_dotenv

from app.github_client import fetch_all_repos


def rmtree_readonly(path):
    def on_error(_func, fpath, _exc_info):
        os.chmod(fpath, stat.S_IWRITE)
        os.unlink(fpath)

    shutil.rmtree(path, onexc=on_error)


def reset_dir(path):
    if os.path.exists(path):
        rmtree_readonly(path)
    os.makedirs(path, exist_ok=True)


async def main():
    load_dotenv()

    github_token = os.environ.get('GITHUB_TOKEN')
    clone_dir = os.environ.get('CLONE_DIR')
    temp_dir = os.environ.get('TEMP_DIR')

    repos = await fetch_all_repos(github_token)
    print(f"Found {len(repos)} repositories.")

    # Clone to local temp directory to avoid Google Drive interference
    reset_dir(temp_dir)

    await asyncio.sleep(1)

    for repo in repos:
        clone_url = repo['clone_url']
        repo_name = repo['name']
        dest_path = os.path.join(temp_dir, repo_name)
        subprocess.run(['git', 'clone', clone_url, dest_path], check=True)

    print("All repositories cloned. Moving to target directory...")

    # Move cloned repos to target directory
    reset_dir(clone_dir)

    for repo in repos:
        repo_name = repo['name']
        src = os.path.join(temp_dir, repo_name)
        dst = os.path.join(clone_dir, repo_name)
        print(f"Copying {repo_name}...")
        shutil.copytree(src, dst)

    rmtree_readonly(temp_dir)

    print("All repositories moved to target directory.")


asyncio.run(main())
