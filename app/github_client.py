import httpx


async def fetch_all_repos(token: str) -> list[dict]:
    url = 'https://api.github.com/user/repos'
    params = {
        'per_page': 100,
        'page': 1,
        'type': 'owner',
    }
    headers = {'Authorization': f'token {token}'}

    repos = []

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            repos.extend(data)
            params['page'] += 1

    return repos
