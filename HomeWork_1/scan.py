import sys
from pathlib import Path


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


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"Images: {image_files}\n")
    print(f"Documents: {document_files}\n")
    print(f"Videos: {video_files}\n")
    print(f"Audios: {audio_files}\n")
    print(f"Archives: {archive_files}\n")
    print(f"Unknown: {unknown_files}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")