import requests
from requests.auth import HTTPBasicAuth

# Токен для авторизации
TOKEN = 'github_token'
USERNAME = 'github_username'
PASSWORD = 'github_password'
BASE_URL = 'https://api.github.com'
YOUR_USERNAME = USERNAME


# 1. Тестирование авторизации с некорректным токеном
def test_invalid_token():
    invalid_token = 'invalid_token_12345'
    url = f'{BASE_URL}/user'
    headers = {
        'Authorization': f'token {invalid_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print("Test passed: Invalid token returns 401 Unauthorized.")
    else:
        print(f"Test failed: Expected 401, got {response.status_code}")


# 2. Создание нового репозитория
def create_repo(repo_name):
    url = f'{BASE_URL}/user/repos'
    headers = {
        'Authorization': f'token {TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "name": repo_name,
        "description": "Test repository",
        "private": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully.")
    else:
        print(f"Failed to create repository: {response.status_code}")


# Удаление репозитория
def delete_repo(repo_name):
    url = f'{BASE_URL}/repos/{YOUR_USERNAME}/{repo_name}'
    headers = {
        'Authorization': f'token {TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Repository '{repo_name}' deleted successfully.")
    else:
        print(f"Failed to delete repository: {response.status_code}")


# 3. Тестирование лимитов запросов (rate limit)
def test_rate_limit():
    url = f'{BASE_URL}/rate_limit'
    headers = {
        'Authorization': f'token {TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        rate_limit_info = response.json()
        print(f"Limit: {rate_limit_info['rate']['limit']}")
        print(f"Remaining: {rate_limit_info['rate']['remaining']}")
        print(f"Resets at: {rate_limit_info['rate']['reset']}")
    else:
        print(f"Failed to fetch rate limit info: {response.status_code}")


# 4. Тестирование ETag для кеширования данных
def test_etag(username):
    url = f'{BASE_URL}/users/{username}'
    headers = {
        'Authorization': f'token {TOKEN}'
    }

    # Первый запрос для получения данных и ETag
    response = requests.get(url, headers=headers)
    if 'ETag' in response.headers:
        etag = response.headers['ETag']
        print(f"ETag received: {etag}")

        # Второй запрос с использованием ETag
        headers['If-None-Match'] = etag
        cached_response = requests.get(url, headers=headers)

        if cached_response.status_code == 304:
            print("Test passed: ETag works correctly, no new data fetched.")
        else:
            print(f"Test failed: Expected 304, got {cached_response.status_code}")
    else:
        print("No ETag found in response headers.")


# 5. Авторизация с помощью OAuth токена
def test_oauth_auth():
    url = f'{BASE_URL}/user'
    headers = {
        'Authorization': f'token {TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        print(f"OAuth Auth Test passed: User logged in as {user_info['login']}.")
    else:
        print(f"OAuth Auth Test failed: {response.status_code}")


# 6. Авторизация с помощью Basic Authentication
def test_basic_auth():
    url = f'{BASE_URL}/user'
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, TOKEN))

    if response.status_code == 200:
        user_info = response.json()
        print(f"Basic Auth Test passed: User logged in as {user_info['login']}.")
    else:
        print(f"Basic Auth Test failed: {response.status_code}")


# Пример вызова тестов
repo_name = "test-repo"

# 1. Тестирование с неверным токеном
test_invalid_token()

# 2. Создание и удаление репозитория
create_repo(repo_name)
delete_repo(repo_name)

# 3. Тестирование лимита запросов
test_rate_limit()

# 4. Тестирование ETag
test_etag('octocat')

# 5. Тестирование OAuth авторизации
test_oauth_auth()

# 6. Тестирование Basic авторизации
test_basic_auth()
