import requests
import configparser
import base64
from tqdm import tqdm
import os

class GitHubUploader:
    def __init__(self):
        self.owner, self.header = self.load_github_credentials()

    def load_github_credentials(self):
        config = configparser.ConfigParser()
        config.read('secrets.ini')
        token = config.get('github', 'token')
        owner = config.get('github', 'owner')
        header = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        return owner, header

    def list_repos(self):
        url = 'https://api.github.com/user/repos'
        response = requests.get(url, headers=self.header)
        repos = response.json()
        return repos

    def create_repo(self, repo_name):
        url = 'https://api.github.com/user/repos'
        data = {
            "name": repo_name,
            "private": False
        }
        response = requests.post(url, headers=self.header, json=data)
        if response.status_code == 201:
            print(f"Repository '{repo_name}' created successfully!")
            return response.json()
        else:
            print(f"Failed to create repository '{repo_name}'. Status code: {response.status_code}")
            return None

    def get_file_sha(self, repo_name, file_path):
        url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{file_path}"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            return response.json()['sha']
        return None

    def upload_file(self, repo_name, file_path, commit_message):
        with open(file_path, "rb") as f:
            file_content = f.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
        relative_path = os.path.relpath(file_path, start='.')
        url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{relative_path}"

        sha = self.get_file_sha(repo_name, relative_path)

        data = {
            "message": commit_message,
            "content": encoded_content,
            "sha": sha
        }

        # Progress bar setup
        with tqdm(total=len(encoded_content), desc=f"Uploading {file_path}", unit='B', unit_scale=True) as pbar:
            response = requests.put(url, headers=self.header, json=data)
            pbar.update(len(encoded_content))

        if response.status_code in [200, 201]:
            print(f"File '{file_path}' uploaded successfully!")
        else:
            print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")

    def upload_directory(self, repo_name, directory_path, commit_message):
        total_size = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(directory_path) for file in files)
        uploaded_size = 0

        with tqdm(total=total_size, desc=f"Uploading directory {directory_path}", unit='B', unit_scale=True) as pbar:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        file_content = f.read()
                    encoded_content = base64.b64encode(file_content).decode("utf-8")
                    relative_path = os.path.relpath(file_path, start='.')
                    url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{relative_path}"

                    sha = self.get_file_sha(repo_name, relative_path)

                    data = {
                        "message": commit_message,
                        "content": encoded_content,
                        "sha": sha
                    }

                    response = requests.put(url, headers=self.header, json=data)
                    if response.status_code in [200, 201]:
                        uploaded_size += len(encoded_content)
                        pbar.update(len(encoded_content))
                    else:
                        print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")

# For testing the upload functionality directly
if __name__ == "__main__":
    uploader = GitHubUploader()
    repos = uploader.list_repos()
    selected_repo = uploader.select_repo(repos)
    print(f"You selected: {selected_repo['name']}")
    file_path = 'your_file.txt'
    commit_message = 'Adding a new file'
    uploader.upload_file(selected_repo['name'], file_path, commit_message)
