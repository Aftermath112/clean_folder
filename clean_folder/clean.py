import re
import shutil
import sys
from pathlib import Path

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p",
               "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

Images = []
Videos = []
Doc = []
Music = []
archives = []
others = []
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": Images,
    "PNG": Images,
    "JPG": Images,
    "SVG": Images,
    "AVI": Videos,
    "MP4": Videos,
    "MOV": Videos,
    "MKV": Videos,
    "TXT": Doc,
    "DOCX": Doc,
    "DOC": Doc,
    "PDF": Doc,
    "XLSX": Doc,
    "PPTX": Doc,
    "MP3": Music,
    "OGG": Music,
    "WAV": Music,
    "AMR": Music,
    "ZIP": archives,
    "GZ": archives,
    "TAR": archives
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
            if item.name not in ("archives", "video", "audio", "documents", "images"):
                # folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
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
    path.replace(target_folder / normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    print(target_folder)
    new_name = normalize(path.name.replace(Path(path).suffix[1:], ''))
    print(new_name)
    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve(path)), str(archive_folder))
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
    scan(folder_path)

    for file in Images:
        hande_file(file, folder_path, "images")

    for file in Doc:
        hande_file(file, folder_path, "documents")

    for file in Music:
        hande_file(file, folder_path, "audio")

    for file in Videos:
        hande_file(file, folder_path, "video")

    for file in archives:
        handle_archive(file, folder_path, "archives")

    for file in others:
        hande_file(file, folder_path, "OTHERS")

    get_folder_objects(folder_path)


def process():
    #print(f"Start in {path}")
    path = sys.argv[1]
    arg = Path(path)
    main(arg)


if __name__ == '__main__':
    process()
