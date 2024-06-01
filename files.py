import os

class FileManager:
    @staticmethod
    def list_files():
        files = os.listdir('.')
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")
        return files

    @staticmethod
    def select_files(files):
        file_indices = input("Enter the numbers of the files you want to upload, separated by commas: ")
        selected_files = [files[int(i) - 1] for i in file_indices.split(',')]
        return selected_files

    @staticmethod
    def get_file_path(file_name):
        return os.path.join(os.getcwd(), file_name)


if __name__ == "__main__":
    # Create an instance of FileManager
    file_manager = FileManager()

    # List files in the current directory
    files = file_manager.list_files()

    # Select files to upload
    selected_files = file_manager.select_files(files)
    print(f"Selected files: {selected_files}")

    # Get the file paths of selected files
    file_paths = [file_manager.get_file_path(file) for file in selected_files]
    print(f"File paths: {file_paths}")
