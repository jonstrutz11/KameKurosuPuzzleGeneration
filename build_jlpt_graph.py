"""Read exported word list from ZKanji and write it to a format usable by
クロスワード　ギバー."""

import pickle

import matplotlib.pyplot as plt
import seaborn as sns

from preprocess_zkanji_wordlist import Entry


if __name__ == '__main__':
    INFILE_PATH = './data/processed_zkanji_entries.pickle'

    with open(INFILE_PATH, 'rb') as infile:
        zkanji_entries = pickle.load(infile)

    zkanji_entries = [zkanji_entries[key] for key in zkanji_entries]

    jlpt_counts = [0, 0, 0, 0, 0, 0]
    jlpt_ranks = [[], [], [], [], [], []]
    for entry in zkanji_entries:
        if entry.jlpt == 'N5':
            jlpt_counts[0] += 1
            jlpt_ranks[0].append(entry.rank)
        elif entry.jlpt == 'N4':
            jlpt_counts[1] += 1
            jlpt_ranks[1].append(entry.rank)
        elif entry.jlpt == 'N3':
            jlpt_counts[2] += 1
            jlpt_ranks[2].append(entry.rank)
        elif entry.jlpt == 'N2':
            jlpt_counts[3] += 1
            jlpt_ranks[3].append(entry.rank)
        elif entry.jlpt == 'N1':
            jlpt_counts[4] += 1
            jlpt_ranks[4].append(entry.rank)
        else:
            jlpt_counts[5] += 1
            jlpt_ranks[5].append(entry.rank)

    for ranks in jlpt_ranks:
        sns.distplot(ranks)
    plt.legend(['N5', 'N4', 'N3', 'N2', 'N1', 'N-'])
    plt.show()
