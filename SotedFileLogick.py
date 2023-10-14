import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


class FileSorter:
    def __init__(self, path):
        self.path = Path(path)
        self.images_tuple = ('.jpeg', '.png', '.jpg', '.svg')
        self.video_tuple = ('.avi', '.mp4', '.mov', '.mkv')
        self.document_tuple = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
        self.audio_tuple = ('.mp3', '.ogg', '.wav', '.amr')
        self.archive_tuple = ('.zip', '.gz', '.tar')
        self.sorting_folders = ('archives', 'video', 'audio', 'documents', 'images', 'unknown type')

    def clean_folders(self):
        for folder in self.path.iterdir():
            if folder.name not in self.sorting_folders and folder.is_dir():
                self._clean_folder(folder)

    def _clean_folder(self, folder):  # Функция рекурсивной очистки пустых папок
        for item in folder.iterdir():
            if item.is_dir():
                self._clean_folder(item)
            if not any(folder.iterdir()):
                folder.rmdir()

    def create_folders(self):  # Функция создания папок для сортировки
        for folder in self.sorting_folders:
            folder_path = self.path / folder
            folder_path.mkdir(exist_ok=True)

    def dearchive(self, file_name):
        path_to_unpack = self.path / 'archives'
        folder_path = path_to_unpack / file_name.stem
        folder_path.mkdir(exist_ok=True)
        if file_name.suffix == '.zip':
            shutil.unpack_archive(file_name, folder_path, format='zip')
        elif file_name.suffix == '.tar':
            shutil.unpack_archive(file_name, folder_path, format='tar')
        elif file_name.suffix == '.gz':
            shutil.unpack_archive(file_name, folder_path, format='gz')

    def sort_file(self, file_name):
        if file_name.suffix in self.document_tuple:
            self._move_file(file_name, 'documents')
        elif file_name.suffix in self.images_tuple:
            self._move_file(file_name, 'images')
        elif file_name.suffix in self.video_tuple:
            self._move_file(file_name, 'video')
        elif file_name.suffix in self.audio_tuple:
            self._move_file(file_name, 'audio')
        elif file_name.suffix in self.archive_tuple:
            self.dearchive(file_name)
        else:
            self._move_file(file_name, 'unknown type')

    def _move_file(self, file_name, folder_name):
        target_folder = self.path / folder_name
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Ошибка при перемещении файла, скорее всего файл {file_name.name} - открыт !!!')

    def parse(self):
        self.create_folders()
        self._parse_files(self.path)
        self.clean_folders()

    def _parse_files(self, folder):
        for item in folder.iterdir():
            if item.is_dir() and item.name not in self.sorting_folders:
                self._parse_files(item)
            elif item.is_file():
                self.sort_file(item)


def select_and_sort_folder():
    def select_folder():
        root = tk.Tk()
        root.withdraw()  # Скрываем главное окно tkinter
        folder_selected = filedialog.askdirectory()
        return folder_selected

    folder_selected = select_folder()
    if not folder_selected:
        print("Вы не выбрали папку для сортировки. Завершение работы.")
        return

    sorter = FileSorter(folder_selected)
    sorter.parse()


if __name__ == "__main__":
    select_and_sort_folder()
