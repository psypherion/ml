import os

class FileManager:
    @staticmethod
    def list_files(directory='.'):
        files = os.listdir(directory)
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")
        return files

    @staticmethod
    def select_files(files):
        try:
            # Display selected files with numbers
            print("\nSelected files and directories:")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")

            # Prompt user to deselect files
            deselect_input = input("Enter numbers or names of files/directories to deselect (comma separated, or '.' for none): ").strip()
            
            # Handle deselection
            if deselect_input == '.':
                return files  # Return all files if '.' is selected
            else:
                deselections = [item.strip() for item in deselect_input.split(',')]
                selected_files = [file for i, file in enumerate(files, start=1) if str(i) not in deselections and file not in deselections]
                return selected_files
        
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid numbers separated by commas.")
            return []

    @staticmethod
    def get_file_path(file_name):
        return os.path.abspath(file_name)
