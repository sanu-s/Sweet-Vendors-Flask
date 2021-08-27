import os
import shutil


def create_dir(file_path):
    os.makedirs(file_path, mode=0o777, exist_ok=True)


def delete_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)


def get_profile_picture_dir(media_root, user_id):
    return os.path.join(media_root, str(user_id), 'picture')


def get_profile_thumbnail_dir(media_root, user_id):
    return os.path.join(media_root, str(user_id), 'picture', 'thumbnail')
