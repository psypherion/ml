from git_uploader import GitHubUploader
from files import FileManager

def main():
    file_manager = FileManager()
    files = file_manager.list_files()
    selected_files = file_manager.select_files(files)
    uploader = GitHubUploader()
    repos = uploader.list_repos()
    selected_repo = uploader.select_repo(repos)
    print(f"You selected: {selected_repo['name']}")
    
    commit_msg = input("Enter commit message: ")
    for file in selected_files:
        uploader.upload_file(selected_repo['name'], file, commit_msg)

if __name__ == "__main__":
    main()
