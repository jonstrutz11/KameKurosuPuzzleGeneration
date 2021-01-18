"""Read exported word list from ZKanji and write it to a format usable by
クロスワード　ギバー."""

from copy import copy
import pickle
import pykakasi


class Entry():
    """An entry for a single word from ZKanji and its reading/frequency/etc."""

    def __init__(self, word: str, readings: [(str, int)], jlpt: str, definition: str, pos: str,
                 rank: int = None, level: int = None):
        self.word = word
        self.readings = readings  # also contains frequency
        self.jlpt = jlpt
        self.definition = definition
        self.pos = pos
        self.rank = rank
        self.level = level

    def __repr__(self):
        return (f'Entry, {self.word} read as {self.readings[0][0]} means "{self.definition}" '
                f'(JLPT: {self.jlpt}, Part-of-Speech: {self.pos})')

    def calc_and_set_level(self):
        """Calculate the level of this word for the app."""
        lowest_freq = self.readings[-1][1]
        if self.jlpt == 'N5':
            self.level = 0
        elif self.jlpt == 'N4' or lowest_freq > 5750:  # top ~500
            self.level = 1
        elif self.jlpt == 'N3' or lowest_freq > 5100:  # top ~2000
            self.level = 2
        elif self.jlpt == 'N2' or lowest_freq > 4500:  # top ~5000
            self.level = 3
        elif self.jlpt == 'N1' or lowest_freq > 3500:  # top ~10000
            self.level = 4
        else:  # top ~25000
            self.level = 5


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

            entry = Entry(word, [(reading, frequency)], jlpt, definition, pos, rank + 1)
            entry.calc_and_set_level()
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
    for i, entry in enumerate(entries):
        if all_words.count(entry.word) > 1:
            if entry.word not in new_words:
                new_entries.append(entry)
                for entry2 in entries[(i + 1):]:
                    if entry.word == entry2.word:
                        entry.readings.append(entry2.readings[0])
                        new_words.append(entry.word)
        else:
            new_entries.append(entry)

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
            kana_reading = entry.readings[0][0][-kana_tail_len:]
            new_word = f'{kanji_part}({kana_reading})'  # add parentheses to word
            new_reading = (kanji_reading, entry.readings[0][1])

            new_entry = Entry(new_word, [new_reading], copy(entry.jlpt), copy(entry.definition),
                              copy(entry.pos), copy(entry.rank), copy(entry.level))
            new_entries.append(new_entry)

    return entries + new_entries


def is_kana(char: str) -> bool:
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


def write_entries_to_dict(outpath: str, entries: [Entry], level: int) -> None:
    """Write entries in dict format required by クロスワード　ギバー software."""
    kks = pykakasi.kakasi()
    kks.setMode('J', 'K')
    kanji_conv = kks.getConverter()
    kks.setMode('H', 'K')
    hiragana_conv = kks.getConverter()

    with open(f'{outpath}_level_{level}.txt', 'w', encoding='utf-8') as outfile:
        for entry in entries:
            if entry.level <= level:
                for reading in entry.readings:
                    if len(entry.readings) > 1 and is_obscure_reading(reading[1], entry.jlpt):
                        continue
                    katakana_reading = hiragana_conv.do(kanji_conv.do(reading[0]))
                    outfile.write(f'{katakana_reading}\t{entry.word}\n')


def is_obscure_reading(frequency, jlpt) -> bool:
    """Whether this reading is obscure for this JLPT level."""
    obscure = False
    if jlpt in ['N5', 'N4'] and frequency <= 5750:
        obscure = True
    elif jlpt == 'N3' and frequency <= 5100:
        obscure = True
    elif jlpt == 'N2' and frequency <= 4500:
        obscure = True
    elif jlpt == 'N1' and frequency <= 3500:
        obscure = True
    return obscure


def delete_singleton_readings(entries: [Entry]) -> [Entry]:
    """Filter out readings of length one as we can't use those in crossword."""
    new_entries = []
    for entry in entries:
        new_readings = []
        for reading in entry.readings:
            if len(reading[0]) <= 1:
                continue
            else:
                new_readings.append(reading)

        if new_readings:
            new_entry = Entry(copy(entry.word), new_readings, copy(entry.jlpt),
                              copy(entry.definition), copy(entry.pos), copy(entry.rank),
                              copy(entry.level))
            new_entries.append(new_entry)

    return new_entries



if __name__ == '__main__':
    INFILE_PATH = './data/AllWords.zkanji.export'
    OUTFILE_PATH_PREFIX = './data/zkanji_outdict'
    PICKLE_PATH = './data/processed_zkanji_entries.pickle'

    zkanji_entries = parse_zkanji_wordlist(INFILE_PATH)
    zkanji_entries = add_verb_stem_readings(zkanji_entries)

    zkanji_entries = delete_singleton_readings(zkanji_entries)

    for level in range(6):  
        write_entries_to_dict(OUTFILE_PATH_PREFIX, zkanji_entries, level)

    # Write all entries to a pickle file for easy lookup later
    final_dict = {}
    kks = pykakasi.kakasi()
    kks.setMode('J', 'K')
    kanji_conv = kks.getConverter()
    kks.setMode('H', 'K')
    hiragana_conv = kks.getConverter()
    for zkanji_entry in zkanji_entries:
        new_readings = []
        for reading in zkanji_entry.readings:
            katakana_reading = hiragana_conv.do(kanji_conv.do(reading[0]))
            new_reading = (katakana_reading, reading[1])
            new_readings.append(new_reading)
        zkanji_entry.readings = new_readings
        if zkanji_entry.word not in zkanji_entries:
            final_dict[zkanji_entry.word] = zkanji_entry
        else:
            print("Warning: duplicate entries exist in final list of entries.")

    with open(PICKLE_PATH, 'wb') as outfile:
        pickle.dump(final_dict, outfile)
