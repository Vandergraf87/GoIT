import shutil
import sys
import scan
import normalize
from pathlib import Path



def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.translate(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize.translate(path.name.replace(".zip", '').replace(".tar", '').replace(".gz", ''))

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

def main(folder_path):
    scan.scan(folder_path)

    for file in scan.image_files:
        hande_file(file, folder_path, "Images")

    for file in scan.document_files:
        hande_file(file, folder_path, "Documents")

    for file in scan.video_files:
        hande_file(file, folder_path, "Videos")

    for file in scan.audio_files:
        hande_file(file, folder_path, "Audios")
        
    for file in scan.unknown_files:
        hande_file(file, folder_path, "Unknown")

    for file in scan.archive_files:
        handle_archive(file, folder_path, "Archives")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    main(arg.resolve())
