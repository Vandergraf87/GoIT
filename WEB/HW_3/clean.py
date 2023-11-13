
import concurrent.futures
import logging
import shutil
import sys
import re
from pathlib import Path


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {} 
    
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def translate(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"



image_files = list()
document_files = list()
video_files = list()
audio_files = list()
archive_files = list()
folders = list()
unknown_files = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": image_files,
    "PNG": image_files,
    "JPG": image_files,
    "SVG": image_files,
    "TXT": document_files,
    "DOCX": document_files,
    "DOC": document_files,
    "PDF": document_files,
    "XLSX": document_files,
    "PPTX": document_files,
    "AVI": video_files,
    "MP4": video_files,
    "MOV": video_files,
    "MKV": video_files,
    "MP3": audio_files,
    "OGG": audio_files,
    "WAV": audio_files,
    "AMR": audio_files,
    "GZ": archive_files,
    "TAR": archive_files,
    "ZIP": archive_files
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("Images", "Videos", "Audios", "Documents", "Archives", "Unknown"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            unknown_files.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                unknown_files.append(new_name)


    print(f"Images: {image_files}\n")
    print(f"Documents: {document_files}\n")
    print(f"Videos: {video_files}\n")
    print(f"Audios: {audio_files}\n")
    print(f"Archives: {archive_files}\n")
    print(f"Unknown: {unknown_files}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")



def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/translate(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = translate(path.name.replace(".zip", '').replace(".tar", '').replace(".gz", ''))

    archive_folder = root_folder / dist / new_name
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

def main():
    path = sys.argv[1]
    folder_path = Path(path)
    scan(folder_path)

    for file in image_files:
        hande_file(file, folder_path, "Images")

    for file in document_files:
        hande_file(file, folder_path, "Documents")

    for file in video_files:
        hande_file(file, folder_path, "Videos")

    for file in audio_files:
        hande_file(file, folder_path, "Audios")
        
    for file in unknown_files:
        hande_file(file, folder_path, "Unknown")

    for file in archive_files:
        handle_archive(file, folder_path, "Archives")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(main(), ))

    logging.debug(results)