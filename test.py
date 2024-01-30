import os

path_storage = os.path.join(os.path.expanduser(
    "~"), r"OneDrive\Área de Trabalho\music\home")

print(path_storage)

os.makedirs(path_storage)
