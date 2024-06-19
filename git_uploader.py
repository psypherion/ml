import requests
import configparser
import base64

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

    def select_repo(self, repos):
        print("Available Repositories:")
        for i, repo in enumerate(repos, start=1):
            print(f"{i}. {repo['name']}")
        while True:
            choice = input("Enter the number of the repository to upload files to: ")
            if choice.isdigit() and 1 <= int(choice) <= len(repos):
                return repos[int(choice) - 1]
            else:
                print("Invalid choice. Please enter a valid number.")

    # def upload_file(self, repo_name, file_path, commit_message):
    #     with open(file_path, "rb") as f:
    #         file_content = f.read()
    #     encoded_content = base64.b64encode(file_content).decode("utf-8")
    #     url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{file_path}"
    #     data = {"message": commit_message, "content": encoded_content}
    #     response = requests.put(url, headers=self.header, json=data)
    #     if response.status_code == 201:
    #         print(f"File '{file_path}' uploaded successfully!")
    #     else:
    #         print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")
    
    def upload_file(self, repo_name, file_path, commit_message):
        with open(file_path, "rb") as f:
            file_content = f.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
        url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{file_path}"
        get_response = requests.get(url, headers=self.header)
        if get_response.status_code == 200:
            sha = get_response.json().get('sha')
            data = {"message": commit_message, "content": encoded_content, "sha": sha}
        else:
            data = {"message": commit_message, "content": encoded_content}
        response = requests.put(url, headers=self.header, json=data)
        if response.status_code in [200, 201]:
            print(f"File '{file_path}' uploaded successfully!")
        else:
            print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")
            
    def create_repo(self, repo_name):
        url = 'https://api.github.com/user/repos'
        data = {'name': repo_name}
        response = requests.post(url, headers=self.header, json=data)
        if response.status_code == 201:
            print(f"Repository {repo_name} created successfully!")
        else:
            print(f"Failed to create repository {repo_name}. Status code: {response.status_code}")





if __name__ == "__main__":
    # Create an instance of GitHubUploader
    uploader = GitHubUploader()

    # List repositories and select a repository
    repos = uploader.list_repos()
    selected_repo = uploader.select_repo(repos)
    print(f"You selected: {selected_repo['name']}")

    # Specify the file path, commit message, and upload the file
    file_path = 'allah.txt'
    commit_message = 'Adding a new file'
    uploader.upload_file(selected_repo['name'], file_path, commit_message)
