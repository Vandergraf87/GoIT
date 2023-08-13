import os
import shutil
import sys

def normalize(text):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'y',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'iu', 'я': 'ia',
    }

    text = text.lower()
    result = []

    for char in text:
        if char in translit_dict:
            result.append(translit_dict[char])
        elif char.isalnum():
            result.append(char)
        else:
            result.append('_')

    return ''.join(result)

def sort_folder(folder_path):
    if not os.listdir(folder_path):
        os.rmdir(folder_path)  # Видаляємо порожню папку
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            file_name, file_ext = os.path.splitext(item)
            new_file_name = normalize(file_name)
            new_file_ext = file_ext.lower()  # Не міняємо розширення
            new_item_name = new_file_name + new_file_ext
            new_item_path = os.path.join(folder_path, new_item_name)

            if os.path.exists(new_item_path):
                duplicate_id = 1
                while os.path.exists(new_item_path):
                    new_item_name = f"{new_file_name}_duplicate{duplicate_id}{new_file_ext}"
                    new_item_path = os.path.join(folder_path, new_item_name)
                    duplicate_id += 1

            os.rename(item_path, new_item_path)

            category = get_category(file_ext[1:].upper())
            category_path = os.path.join(folder_path, category)

            if not os.path.exists(category_path):
                os.makedirs(category_path)

            new_item_path_in_category = os.path.join(category_path, new_item_name)
            if os.path.exists(new_item_path_in_category):
                duplicate_id = 1
                while os.path.exists(new_item_path_in_category):
                    new_item_name = f"{new_file_name}_duplicate{duplicate_id}{new_file_ext}"
                    new_item_path_in_category = os.path.join(category_path, new_item_name)
                    duplicate_id += 1

            shutil.move(new_item_path, new_item_path_in_category)
        
        elif os.path.isdir(item_path) and item not in EXTENSIONS_DICT:
            sort_folder(item_path)

def get_category(extension):
    for category, ext_list in EXTENSIONS_DICT.items():
        if extension in ext_list:
            return category
    return 'unknown'

EXTENSIONS_DICT = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR']
}

def main():
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        return

    folder_path = sys.argv[1]
    known_extensions = set()
    unknown_extensions = set()

    sort_folder(folder_path, known_extensions, unknown_extensions)

    print("Sorting completed.")
    print("Known Extensions:")
    print(", ".join(known_extensions))
    print("\nUnknown Extensions:")
    print(", ".join(unknown_extensions))

if __name__ == "__main__":
    main()