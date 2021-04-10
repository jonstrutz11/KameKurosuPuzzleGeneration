"""Read exported word list from ZKanji and write it to a format usable by
クロスワード　ギバー."""

import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from preprocess_zkanji_wordlist import Entry  # required for pickle

if __name__ == '__main__':
    INFILE_PATH = './data/processed_zkanji_entries.pickle'

    with open(INFILE_PATH, 'rb') as infile:
        zkanji_entries = pickle.load(infile)

    zkanji_entries = [zkanji_entries[key] for key in zkanji_entries]

    jlpt_counts = [0, 0, 0, 0, 0, 0]
    jlpt_ranks = [[], [], [], [], [], []]
    jlpt_levels = ['N5', 'N4', 'N3', 'N2', 'N1', 'N-']
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

    ranks_col = []
    jlpt_level_col = []
    for jlpt_level, ranks in zip(jlpt_levels, jlpt_ranks):
        ranks_col += ranks
        jlpt_level_col += [jlpt_level] * len(ranks)

    df = pd.DataFrame()
    df['JLPT Level'] = jlpt_level_col
    df['Word Frequency Rank'] = ranks_col

    # Plot
    sns.set(font_scale=2.0)
    fig, ax = plt.subplots(nrows=1, ncols=1)

    sns.histplot(data=df, x='Word Frequency Rank', hue='JLPT Level', bins=range(0, 25001, 1000),
                 multiple='stack', ax=ax)

    ax.set_xlabel('Word Frequency Rank (lower = more frequent)')
    ax.set_xlim(0, 25000)

    ax.set_ylabel('Number of Words')

    ax.set_title('Word Frequency Histogram by JLPT Level')

    plt.show()
