
import os
import json

def generate_word_objects(data):
    words = []
    past_across_readings = []
    past_down_readings = []
    for direction in ['h', 'v']:
        for hint in data['hints'][direction]:
            across = (direction == 'h')
            reading = hint[1]
            n = calc_n(reading, across, past_across_readings, past_down_readings)
            try:
                row, col = get_coords(data['cell_data'], reading, across, n)
            except TypeError:
                print(data['cell_data'], reading, across, n)
            word = {
                'across': across,
                'clue_number': hint[0],
                'row': row,
                'col': col,
                'kanji_form': hint[2],
                'reading': reading
            }
            words.append(word)
    return words


def calc_n(reading, across, past_across_readings, past_down_readings):
    """Account for duplicate readings in puzzle when searching for reading position."""
    if across:
        return past_across_readings.count(reading)
    else:
        return past_down_readings.count(reading)


def get_coords(cell_data, reading, across, n):
    found_n = 0
    if across:
        for row_i, row in enumerate(cell_data):
            for col in find_all(row, reading):
                if bounded(cell_data, row_i, col, across, reading):
                    found_n += 1
                    if found_n > n:                    
                        return row_i, col
    else:
        new_cell_data = conv_cell_data_to_cols(cell_data)
        for col_i, col in enumerate(new_cell_data):
            for row in find_all(col, reading):
                if bounded(new_cell_data, row, col_i, across, reading):
                    found_n += 1
                    if found_n > n:
                        return row, col_i


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


def bounded(data, row, col, across, reading):
    """Check that word is bounded by black squares or edge."""
    word_len = len(reading)
    if across:
        final_col = col + word_len - 1
        # on left side of puzzle
        if col == 0 and final_col + 1 < len(data[row]) and data[row][final_col + 1] == '■':
            return True
        # on right side of puzzle
        elif final_col + 1 == len(data[row]) and data[row][col - 1] == '■':
            return True
        # in middle of puzzle
        elif data[row][col - 1] == '■' and final_col + 1 < len(data[row]) and data[row][final_col + 1] == '■':
            return True
        # entire width of puzzle
        elif col == 0 and final_col + 1 == len(data[row]):
            return True
        else:
            return False
    else:
        final_row = row + word_len - 1
        # at top of puzzle
        if row == 0 and final_row + 1 < len(data[col]) and data[col][final_row + 1] == '■':
            return True
        # at bottom of puzzle
        elif final_row + 1 == len(data[col]) and data[col][row - 1] == '■':
            return True
        # in middle of puzzle
        elif data[col][row - 1] == '■' and final_row + 1 < len(data[col]) and data[col][final_row + 1] == '■':
            return True
        # entire height of puzzle
        elif row == 0 and final_row + 1 == len(data[col]):
            return True
        else:
            return False


def conv_cell_data_to_cols(cell_data):
    new_cell_data = ['' for _ in range(len(cell_data[0]))]
    for row in cell_data:
        for col_i, char in enumerate(row):
            new_cell_data[col_i] += char
    return new_cell_data


def add_leading_zeros(number):
    """Add zeros such that number is 4 digits."""
    if not 0 <= int(number) <= 9999:
        raise ValueError(f'Number, {number}, must be between 0 and 9999, inclusive.')

    str_num = str(number)

    if len(str_num) == 1:
        str_num = '000' + str_num
    elif len(str_num) == 2:
        str_num = '00' + str_num
    elif len(str_num) == 3:
        str_num = '0' + str_num

    return str_num


for dir_num in range(6):
    current_dir = f'./data/{dir_num}'
    for filename in sorted(os.listdir(current_dir)):
        filepath = os.path.join(current_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

        file_num = filename.split('.')[0].split('-')[1]
        new_json = {}
        new_json['number'] = int(file_num)

        file_num = add_leading_zeros(file_num)
        
        new_json['id'] = f'{dir_num}-{file_num}'
        new_json['level'] = dir_num

        new_json['words'] = generate_word_objects(data)

        with open(f'data_processed/{dir_num}-{file_num}.json', 'w', encoding='utf-8') as outfile:
            json.dump(new_json, outfile, ensure_ascii=False)
