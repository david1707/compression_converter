import os
import shutil
import subprocess
import py7zr
from zipfile import ZipFile

FOLDER_FILES = os.listdir(path='.')
CURRENT_PATH = os.path.abspath(os.getcwd())

ROMS_LIST_ZIP = [file for file in FOLDER_FILES if file.endswith('.zip')]
ROMS_LIST_7Z = [file for file in FOLDER_FILES if file.endswith('.7z')]


def extract_zip_files(roms_list):
    for rom in roms_list:
        folder_relative_path = os.path.join(CURRENT_PATH, rom.split('.')[0])

        # TODO: Check if folder exists. If not, extract, else, continue
        with ZipFile(rom, 'r') as zf:
            zf.extractall(folder_relative_path)

    print('ALL ZIP FILES EXTRACTED!')


def extract_7z_files(roms_list):
    for rom in roms_list:

        # TODO: Check if folder exists. If not, extract, else, continue
        with py7zr.SevenZipFile(rom, 'r') as archive:
            archive.extractall()

    print('ALL 7Z FILES EXTRACTED')


def compress_zip_files():
    folder_list = get_folder_list()
    for folder in folder_list:
        zf = ZipFile(f'{folder}.zip', "w")
        folder_relative_path = os.path.join(CURRENT_PATH, folder)
        for dirname, subdirs, files in os.walk(folder_relative_path):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(folder_relative_path) + 1:]
                zf.write(absname, arcname)
    print('ALL FOLDERS COMPRESSED!')


def compress_7z_files():
    folder_list = get_folder_list()
    for folder in folder_list:

        # TODO: This process is SLOW; look for a better way or use terminal commando with subprocess
        with py7zr.SevenZipFile(folder + ".7z", 'w') as archive:
            archive.writeall(os.path.join(CURRENT_PATH, folder))

    print('ALL FOLDERS COMPRESSED!')


# Helper functions

def get_folder_list():
    return [folder for folder in os.listdir(
        path='.') if os.path.isdir(os.path.join(CURRENT_PATH, folder)) and folder != '.git']


def clean_temporary_folders():
    folders_list = [folder for folder in os.listdir(
        path='.') if os.path.isdir(os.path.join(CURRENT_PATH, folder))]

    for folder in folders_list:
        try:
            shutil.rmtree(os.path.join(CURRENT_PATH, folder))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def main():
    extract_zip_files(ROMS_LIST_ZIP)
    compress_7z_files()
    # extract_7z_files(ROMS_LIST_7Z)
    # compress_zip_files()
    # clean_temporary_folders()


if __name__ == "__main__":
    main()

# TODO: Add try/catch and other security
# TODO: Add extract all .zip files mode
# TODO: Add extract all .7z files mode
# TODO: Add extract all .zip and .7z files mode
# TODO: Clean the code
# TODO: Pass arguments via terminal
# TODO: Create the inverse process; from 7z to zip
# TODO: Create a semi-UI to ask the user which process to do
# TODO: Add progress bar
