"""Count # unique words in a set of puzzles"""

import os
import json


for level in range(6):
    print(f'\n\nResults for Level {level}')

    INFILE_PATH = f'./data/{level}/'

    all_puzzle_words = []

    for filepath in os.listdir(INFILE_PATH):
        puzzles = []
        puzzle_words = []

        with open(INFILE_PATH + filepath, 'rb') as infile:
            data = json.load(infile)

        h_hints = data['hints']['h']
        v_hints = data['hints']['v']

        for hints in [h_hints, v_hints]:
            for hint in hints:
                word = hint[2]
                puzzle_words.append(word)

        all_puzzle_words += puzzle_words

        puzzles.append(puzzle_words)


    print(len(set(all_puzzle_words)), len(all_puzzle_words))

    counts = [all_puzzle_words.count(word) for word in all_puzzle_words]
    #print(counts)
    new_counts = [counts.count(count) for count in counts]

    #print(new_counts)

    count_dict = {}
    for count, new_count in zip(counts, new_counts):
        count_dict[count] = new_count

    for key in sorted(count_dict):
        print(key, int(count_dict[key] / key))


    for i, puzzle1 in enumerate(puzzles):
        matches = 0
        for j, puzzle2 in enumerate(puzzles[i+1:]):
            for word in puzzle2:
                if word in puzzle1:
                    matches += 1
                else:
                    continue
            if matches == len(puzzle2):
                print(f'Duplicate puzzle {i+1, j+1}! {puzzle1}')
