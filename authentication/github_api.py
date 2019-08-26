import requests, json

API_URL = "https://api.github.com"

def get_user_data(user, token):
    return json.loads(requests.get(f"{API_URL}/users/{user.username}", headers={'Authorization': f'token {token}'}).content)

def get_user_repositories(user, token):
    return json.loads(requests.get(f"{API_URL}/users/{user.username}/repos", headers={'Authorization': f'token {token}'}).content)

def get_repository_info(user, repository, token):
    print(f"{API_URL}/repos/{user.username}/{repository}")
    return json.loads(requests.get(f"{API_URL}/repos/{user.username}/{repository}",  headers={'Authorization': f'token {token}'}).content)

def get_repository_tags(user, repository, token):
    print(f"{API_URL}/repos/{user.username}/{repository}")
    return json.loads(requests.get(f"{API_URL}/repos/{user.username}/{repository}/topics",  headers={'Authorization': f'token {token}', 'Accept': "application/vnd.github.mercy-preview+json"}).content)

def update_repository_tags(user, repository, token, topics):
    url = f"{API_URL}/repos/{user.username}/{repository}/topics"
    header = { "Authorization": f"token {token}", 'Accept': "application/vnd.github.mercy-preview+json"}
    resp = requests.put(url, json={"names": topics}, headers=header)
    print(resp.headers)
    return json.loads(resp.content)

def filter_repositories(user, token, topics):
    resp = requests.get(f"https://api.github.com/search/repositories?q=topic:{topics}+user:{user.username}", headers={'Authorization': f'token {token}', 'Accept': "application/vnd.github.mercy-preview+json"})
    try:
        lista = json.loads(resp.content)['items']
    except KeyError:
        lista = []
        
    # concat fork repositories
    resp = requests.get(f"https://api.github.com/search/repositories?q=topic:{topics}+user:{user.username}+fork:true", headers={'Authorization': f'token {token}', 'Accept': "application/vnd.github.mercy-preview+json"})
    try:
        for el in json.loads(resp.content)['items']:
            if el not in lista:
                lista.append(el)
    except KeyError:
        pass
    return lista