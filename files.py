import os
import logging

class FileManager:
    @staticmethod
    def list_files(directory='.'):
        try:
            files = os.listdir(directory)
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")
            return files
        except Exception as e:
            logging.error(f"Error listing files in directory '{directory}': {e}")
            return []

    @staticmethod
    def select_files(files):
        try:
            print("\nSelected files and directories:")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")

            deselect_input = input("Enter numbers or names of files/directories to deselect (comma separated, or '.' for none): ").strip()
            if deselect_input == '.':
                return files
            else:
                deselections = [item.strip() for item in deselect_input.split(',')]
                selected_files = [file for i, file in enumerate(files, start=1) if str(i) not in deselections and file not in deselections]
                return selected_files
        except (ValueError, IndexError) as e:
            logging.error(f"Invalid input for deselection: {e}")
            return []

    @staticmethod
    def get_file_path(file_name):
        return os.path.abspath(file_name)
