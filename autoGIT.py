import argparse
import os
from git_uploader import GitHubUploader
from files import FileManager

def initialize_git_repo(path):
    os.system(f"git init {path}")

def main():
    parser = argparse.ArgumentParser(description="Auto Git uploader")
    parser.add_argument('-p', '--path', nargs='*', default=['.'], help="Path to files or directories to upload")
    args = parser.parse_args()

    # Initialize git repo
    initialize_git_repo('.')

    file_manager = FileManager()
    uploader = GitHubUploader()

    repos = uploader.list_repos()
    print("Available Repositories:")
    print("0. Create a new repository")
    for i, repo in enumerate(repos, start=1):
        print(f"{i}. {repo['name']}")

    choice = input("Enter the number of the repository to upload files to (default 0): ")
    if choice == '' or choice == '0':
        repo_name = input("Enter the name of the new repository: ")
        selected_repo = uploader.create_repo(repo_name)
    else:
        selected_repo = repos[int(choice) - 1]

    if args.path:
        selected_files = args.path
        if '.' in selected_files:
            selected_files = file_manager.list_files()
        else:
            selected_files = [file for file in selected_files if os.path.exists(file)]

        print(f"You selected: {selected_files}")
        confirm = input("Do you want to upload these files? (Y/n): ")
        if confirm.lower() == 'n':
            selected_files = file_manager.select_files(selected_files)

    else:
        selected_files = file_manager.select_files(file_manager.list_files())

    if not selected_files:
        print("No files selected. Exiting.")
        return

    commit_msg = input("Enter commit message: ")
    for path in selected_files:
        if os.path.isdir(path):
            print(f"Uploading directory: {path}")
            uploader.upload_directory(selected_repo['name'], path, commit_msg)
        else:
            print(f"Uploading file: {path}")
            uploader.upload_file(selected_repo['name'], path, commit_msg)

if __name__ == "__main__":
    main()
