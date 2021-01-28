"""Rename crossword files so that they are all unique (required by iOS filesystem) and end in .json"""

import os

for dir_num in range(6):
    current_dir = f'./data/{dir_num}'
    for filename in os.listdir(current_dir):
        file_num = filename.split('.')[0]
        new_filename = f'{dir_num}-{file_num}.json'
        old_filepath = os.path.join(current_dir, filename)
        new_filepath = os.path.join(current_dir, new_filename)
        os.rename(old_filepath, new_filepath)
