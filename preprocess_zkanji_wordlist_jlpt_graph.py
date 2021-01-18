"""Read exported word list from ZKanji and write it to a format usable by
クロスワード　ギバー."""

from copy import copy


class Entry():
    """An entry for a single word from ZKanji and its reading/frequency/etc."""

    def __init__(self, word: str, readings: [(str, int)], jlpt: str, definition: str, pos: str,
                 level: str = None, rank: int = None):
        self.word = word
        self.readings = readings  # also contains frequency
        self.jlpt = jlpt
        self.definition = definition
        self.pos = pos
        self.level = level
        self.rank = rank

    def __repr__(self):
        return (f'Entry, {self.word} read as {self.readings[0][0]} means "{self.definition}" '
                f'(JLPT: {self.jlpt}, Part-of-Speech: {self.pos})')

    def calc_level(self):
        """Calculate the level of this word for the app."""
        if self.jlpt == 'N5' or self.rank <= 1000:
            self.level = 'Beginner I'
        elif self.jlpt == 'N4' or self.rank <= 2000:
            self.level = 'Beginner II'
        elif self.jljpt == 'N3' or self.rank <= 4000:
            pass


def parse_zkanji_wordlist(filepath: str) -> [Entry]:
    """Parse zkanji export data in input file."""
    with open(filepath, 'r', encoding='utf-8') as infile:
        lines = [line.strip() for line in infile.readlines()]

    data_started = False
    entries = []
    for rank, line in enumerate(lines):
        if line == '[Words]':
            data_started = True
            continue
        if line and data_started:
            word, reading, frequency_string, *meaning_data = line.split(' ')
            frequency = int(frequency_string.replace('F', ''))

            meaning_data = ' '.join(meaning_data)
            jlpt = meaning_data.split('G(\t')[1].split('\t')[0]
            definition = meaning_data.split('\t')[1]
            if 'MT' in meaning_data:
                pos = meaning_data.split('MT')[1].split(' ')[0]
            else:
                pos = None

            entry = Entry(word, [(reading, frequency)], jlpt, definition, pos, None, rank + 1)
            entries.append(entry)

    entries = combine_words_w_multiple_readings(entries)
    return entries


def combine_words_w_multiple_readings(entries) -> [Entry]:
    """Some words like 行き can be read multiple ways (e.g. ゆき or いき), but
    are separate entries in the zkanji data. This function combines these
    entries into one with multiple readings."""
    new_entries = []
    all_words = [entry.word for entry in entries]
    new_words = []
    for i, entry1 in enumerate(entries):
        if all_words.count(entry1.word) > 1:
            if entry1.word not in new_words:
                new_entries.append(entry1)
                for entry2 in entries[(i + 1):]:
                    if entry1.word == entry2.word:
                        entry1.readings.append(entry2.readings[0])
                        new_words.append(entry1.word)
        else:
            new_entries.append(entry1)

    return new_entries


def add_verb_stem_readings(entries) -> [Entry]:
    """Since most verbs end with same characters (e.g. る), make it so we
    copy those entries and change the readings to just the verb stem. This
    gives us more options for making crosswords. For example, 教える, read as
    おしえる, would be converted to 教(える) and its assigned reading would be
    just おし."""
    new_entries = []
    for entry in entries:
        if entry.pos and ('-u' in entry.pos or '-ru' in entry.pos or 'aux.v.' in entry.pos):
            kana_tail_len = 0
            for char in entry.word[::-1]:
                if is_kana(char):
                    kana_tail_len += 1
                else:
                    break

            kanji_part = entry.word[0:-kana_tail_len]
            kanji_reading = entry.readings[0][0][0:-kana_tail_len]
            kana_reading = entry.readings[0][0][kana_tail_len:]
            new_word = f'{kanji_part}({kana_reading})'  # add parentheses to word
            new_reading = (kanji_reading, entry.readings[0][1])

            new_entry = Entry(new_word, new_reading, copy(entry.jlpt),
                              copy(entry.definition), copy(entry.pos), copy(entry.level),
                              copy(entry.rank))
            new_entries.append(new_entry)

    return entries + new_entries


def is_kana(char):
    """Check if a character is hiragana or katakana.

    Parameters
    ----------
    char : str of len 1
        Character to check.

    Returns
    -------
    kana : bool
        True if kana, False otherwise.
    """
    kana = False
    codepoint = ord(char)
    if 12353 <= codepoint <= 12545:
        kana = True
    return kana


if __name__ == '__main__':
    INFILE_PATH = './data/AllWords.zkanji.export'

    zkanji_entries = parse_zkanji_wordlist(INFILE_PATH)

    print(zkanji_entries[6])

    zkanji_entries = add_verb_stem_readings(zkanji_entries)

    import seaborn as sns
    import matplotlib.pyplot as plt

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