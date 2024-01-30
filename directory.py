from messager import Messager
import os


class Directory():
    def __init__(self):
        self.messager = Messager()

    def create_folder(self, path_storage, name):
        file_folder = os.path.join(path_storage, f"{name}")
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)

        return file_folder

    def create_directory(self, name):
        path_storage = os.path.join(os.path.expanduser(
            "~"), "OneDrive")
        if os.path.exists(path_storage):
            directory_pt = os.path.join(path_storage, "Área de Trabalho")
            directory_en = os.path.join(path_storage, "Desktop")

            if os.path.exists(directory_pt):
                path_storage = directory_pt
            elif os.path.exists(directory_en):
                path_storage = directory_en

            return self.create_folder(path_storage, name)

        path_storage = os.path.join(os.path.expanduser(
            "~"), "Desktop")
        if os.path.exists(path_storage):
            return self.create_folder(path_storage, name)

        path_storage = os.path.join(os.path.expanduser(
            "~"), "Área de Trabalho")
        if os.path.exists(path_storage):
            return self.create_folder(path_storage, name)

        path_storage = os.path.join(os.path.expanduser(
            "~"), "Area de Trabalho")
        if os.path.exists(path_storage):
            return self.create_folder(path_storage, name)
