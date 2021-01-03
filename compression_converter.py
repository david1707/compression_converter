import os
import shutil
import subprocess
import py7zr
from zipfile import ZipFile

FOLDER_FILES = os.listdir(path='.')
CURRENT_PATH = os.path.abspath(os.getcwd())

ROMS_LIST = [file for file in FOLDER_FILES if file.endswith('.zip')]


def extract_zip_files(roms_list):
    for rom in roms_list:
        folder_relative_path = os.path.join(CURRENT_PATH, rom.split('.')[0])

        # TODO: Check if folder exists. If not, extract, else, continue
        with ZipFile(rom, 'r') as zf:
            zf.extractall(folder_relative_path)

    print('ALL FILES EXTRACTED!')


def compress_7z_files():
    folders_list = [folder for folder in os.listdir(
        path='.') if os.path.isdir(os.path.join(CURRENT_PATH, folder))]
    for folder in folders_list:

        # TODO: This process is SLOW; look for a better way or use terminal commando with subprocess
        with py7zr.SevenZipFile(folder + ".7z", 'w') as archive:
            archive.writeall(os.path.join(CURRENT_PATH, folder))

    print('ALL FOLDERS COMPRESSED!')


def clean_temporary_folders():
    folders_list = [folder for folder in os.listdir(
        path='.') if os.path.isdir(os.path.join(CURRENT_PATH, folder))]

    for folder in folders_list:
        try:
            shutil.rmtree(os.path.join(CURRENT_PATH, folder))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def main():
    extract_zip_files(ROMS_LIST)
    compress_7z_files()
    clean_temporary_folders()


if __name__ == "__main__":
    main()

# TODO: Pass arguments via terminal
# TODO: Create the inverse process; from 7z to zip
# TODO: Create a semi-UI to ask the user which process to do
# TODO: Add progress bar