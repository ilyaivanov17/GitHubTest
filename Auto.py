import requests

# Токен для авторизации (если нужен)
TOKEN = 'github_token'

# Базовый URL API GitHub
BASE_URL = 'https://api.github.com'

# Функция для получения информации о пользователе
def get_user_info(username):
    url = f'{BASE_URL}/users/{username}'
    headers = {
        'Authorization': f'token {TOKEN}'
    }
    response = requests.get(url, headers=headers)

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        user_data = response.json()
        print(f"User: {user_data['login']}")
        print(f"Name: {user_data['name']}")
        print(f"Public Repos: {user_data['public_repos']}")
    else:
        print(f"Failed to fetch user info: {response.status_code}")

# Функция для получения репозиториев пользователя
def get_user_repos(username):
    url = f'{BASE_URL}/users/{username}/repos'
    headers = {
        'Authorization': f'token {TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            print(f"Repo Name: {repo['name']}, Stars: {repo['stargazers_count']}")
    else:
        print(f"Failed to fetch repos: {response.status_code}")

# Пример вызова функций
username = 'octocat'  # GitHub username
get_user_info(username)
get_user_repos(username)
