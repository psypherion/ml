import os
import argparse
from git_uploader import GitHubUploader
from files import FileManager

def upload_directory(uploader, repo_name, directory, commit_msg):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            uploader.upload_file(repo_name, file_path, commit_msg)

def main():
    parser = argparse.ArgumentParser(description='Auto upload to GitHub.')
    parser.add_argument('-p', '--path', type=str, default='.', help='Path to upload')
    args = parser.parse_args()

    file_manager = FileManager()
    uploader = GitHubUploader()
    repos = uploader.list_repos()
    selected_repo = uploader.select_repo(repos)
    print(f"You selected: {selected_repo['name']}")

    commit_msg = input("Enter commit message: ")
    if os.path.isdir(args.path):
        upload_directory(uploader, selected_repo['name'], args.path, commit_msg)
    else:
        uploader.upload_file(selected_repo['name'], args.path, commit_msg)

if __name__ == "__main__":
    main()
