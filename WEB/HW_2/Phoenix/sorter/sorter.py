import re
import sys
from pathlib import Path
import shutil


UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}
images = []
documents = []
audio = []
video = []
archives = []
others = list()
unknown = set()
extensions = set()
folders = list()

registered_extensions = {
    "JPEG": images,
    "PNG": images,
    "JPG": images,
    "SVG": images,
    'AVI':  video,
    'MP4': video,
    'MOV': video,
    'MKV': video,
    'DOC': documents,
    'PDF': documents, 
    'XLSX': documents, 
    'PPTX': documents,
    "TXT": documents,
    "DOCX": documents,
    'MP3': audio, 
    'OGG': audio, 
    'WAV': audio, 
    'AMR': audio,
    "ZIP": archives,
    'GZ': archives, 
    'TAR': archives
}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"

    
def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("DOCUMENTS", "AUDIO", "VIDEO", "ARCHIVE", "IMAGES", "OTHER"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)



def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", '').replace(".tar", '').replace(".gz", ''))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(path, archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def sorter(dir_path):
    print(f"Start in {dir_path}")

    folder_path = Path(dir_path)
    
    scan(folder_path)
    for file in images:
        hande_file(file, folder_path, "IMAGES")

    for file in documents:
        hande_file(file, folder_path, "DOCUMENTS")

    for file in audio:
        hande_file(file, folder_path, "AUDIO")

    for file in video:
        hande_file(file, folder_path, "VIDEO")

    for file in others:
        hande_file(file, folder_path, "OTHERS")

    for file in archives:
        handle_archive(file, folder_path, "ARCHIVE")

    get_folder_objects(folder_path)

