"""Combine processed data into one big JSON file."""

import os
import json

VERSION = "0.1"

PROCESSED_DATA_DIR = './data_processed'
OUTFILE = './KameKurosuPuzzleData.json'

LEVEL_NAMES_DICT = {
    0: 'Beginner I',
    1: 'Beginner II',
    2: 'Intermediate I',
    3: 'Intermediate II',
    4: 'Advanced I',
    5: 'Advanced II'
}

LEVEL_ROWS_DICT = {
    0: 6,
    1: 7,
    2: 8,
    3: 8,
    4: 8,
    5: 8
}

LEVEL_COLS_DICT = {
    0: 7,
    1: 8,
    2: 9,
    3: 9,
    4: 9,
    5: 9
}

level_data = []
for level_id in range(6):
    new_level = {}
    new_level['id'] = level_id
    new_level['name'] = LEVEL_NAMES_DICT[level_id]
    new_level['nrows'] = LEVEL_ROWS_DICT[level_id]
    new_level['ncols'] = LEVEL_COLS_DICT[level_id]
    new_level['puzzles'] = []
    level_data.append(new_level)

new_json = {'level_data': level_data, 'version': VERSION}

for filename in sorted(os.listdir(PROCESSED_DATA_DIR)):
    if not filename.endswith('.json'):
        continue

    filepath = os.path.join(PROCESSED_DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as infile:
        puzzle_data = json.load(infile)
    level_id = puzzle_data['level']

    new_json['level_data'][level_id]['puzzles'].append(puzzle_data)

with open(OUTFILE, 'w', encoding='utf-8') as outfile:
    json.dump(new_json, outfile, ensure_ascii=False)
