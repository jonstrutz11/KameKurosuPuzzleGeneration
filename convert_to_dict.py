"""Takes in a list of Japanese words, converts them all to katakana, and then
converts all katakana characters to ASCII code points."""


from jamdict import Jamdict
import pykakasi


def load_dictionary(filepath):
    """Load word list (dictionary) from text file.

    Parameters
    ----------
    filepath : str
        Path to dictionary text file.

    Returns
    -------
    word_list : str
        List of words in dictionary.
    """
    with open(filepath, 'r', encoding='utf-8') as infile:
        word_list = infile.readlines()
        word_list = [word.rstrip() for word in word_list]
    return word_list


def initial_filter_words(words, word_limit=None, min_length=1, max_length=10):
    """Filter words based on a limit and undesirable characters.

    Parameters
    ----------
    words : list
        List of words to filter.
    word_limit : int, optional (default: None)
        Maximum number of words to keep. If word_limit=10, only keeps the first
        10 words in the words list. If None (default), keeps all words.
    min_length : int, optional (default: 1)
        Minimum allowed word length.
    max_length : int, optional (default: 10)
        Maximum allowed word length.

    Returns
    -------
    filtered_words : list
        Filtered list of words.
    """
    filtered_words = [word for word in words if len(word) >= min_length
                      and len(word) <= max_length]
    if word_limit:
        filtered_words = filtered_words[:word_limit]
    # Replace て-form verb stems with dictionary form
    filtered_words = [godan_dict_form(word) if godan_verb_stem(word) else word
                      for word in filtered_words]
    filtered_words = [word + 'る' if ichidan_verb_stem(word) else word
                      for word in filtered_words]
    return filtered_words


def godan_verb_stem(word):
    """Determine whether word is a godan て-form verb stem (e.g. 言っ).

    Parameters
    ----------
    word : str
        Japanese word.

    Returns
    -------
    godan : bool
        True if godan, False if not.
    """
    possible_endings = 'っしいん'
    godan = any([word.endswith(ending) for ending in possible_endings])
    return godan


def godan_dict_form(word):
    """Replace verb stem with dictionary form for godan verbs.

    Parameters
    ----------
    word : str
        Japanese word (godan verb stem).

    Returns
    -------
    dict_form : str
        Japanese word (dictionary form godan verb).
    """
    assert word.endswith('っ')
    with open('godan_verb_stems.txt', 'r', encoding='utf-8') as infile:
        godan_map = {line.split(',')[0]: line.split(',')[1]
                     for line in infile.readlines()}
        try:
            dict_form = godan_map[word].strip()
        except KeyError:
            print(f'Warning: Dictionary form not found for {word}')
            dict_form = word
    return dict_form


def ichidan_verb_stem(word):
    """Determine whether word is an ichidan て-form verb stem (e.g. 食べ).

    Parameters
    ----------
    word : str
        Japanese word

    Returns
    -------
    ichidan : bool
        True if ichidan, False if not.
    """
    ichidan = False
    with open('ichidan_verb_stems.txt', 'r', encoding='utf-8') as infile:
        ichidan_verb_stems = [l.rstrip() for l in infile.readlines()]
    if word in ichidan_verb_stems:
        ichidan = True
    return ichidan


def convert_wordlist_to_katakana(japanese_word_list):
    """Convert word (containing kanji, hiragana, katakana) to katakana only.

    Parameters
    ----------
    japanese_word_list : list
        Japanese list of words. Can contain kanji (e.g. 健康),
        hiragana (e.g. ひらがな), katakana (e.g. カタカナ), or a mixture of
        these (e.g. 健康する).

    Returns
    -------
    katakana_word_list : list
        List of all words, but now in katakana. For example, 健康 becomes
        ケンコウ.
    """
    kks = pykakasi.kakasi()
    kks.setMode('J', 'K')
    kanji_conv = kks.getConverter()
    kks.setMode('H', 'K')
    hiragana_conv = kks.getConverter()

    katakana_word_list = []
    for word in japanese_word_list:
        katakana_word = hiragana_conv.do(kanji_conv.do(word))
        katakana_word_list.append(katakana_word)

    return katakana_word_list


def create_dictionary_file(filepath, clues, answers):
    """Create a .dic file containing answers and clues.

    Parameters
    ----------
    filepath : str
        Path to write dictionary file at.
    clues : list
        Clues for answers (in same order).
    answers : list
        Answers for clues (in same order).
    """
    with open(filepath, 'w', encoding='utf-8') as outfile:
        for clue, answer in zip(clues, answers):
            outfile.write(answer)
            outfile.write('\t')
            outfile.write(clue)
            outfile.write('\n')


def filter_words(japanese_words, katakana_words, kana_limit=1.0,
                 max_length=10, duplicates_allowed=False):
    """Filter words from japanese words (and their katakana readings).

    Parameters
    ----------
    japanese_words : list
        Words that may contain kanji, hiragana, and/or katakana.
    katakana_words : list
        Katakana readings of japanese_words.
    kana_limit : float, optional (default: 1.0)
        Fraction of a given word that can have kana (rather than kanji). If set
        to 0.0, filters out any words containing any kana. If set to 1.0
        (default), the entire word can be kana.
    max_length : int, optional (default: 10)
        Maximum length of katakana reading.
    duplicates_allowed : bool (default: False)
        If False, removes duplicate entries in word list.

    Returns
    -------
    japanese_words_filtered : list
        Words that only contain kanji.
    katakana_words_filtered : list
        Katakana readings of japanese_words_kanji.
    """
    japanese_words_filtered = []
    katakana_words_filtered = []
    for jp_word, kk_word in zip(japanese_words, katakana_words):
        filter_out = False

        n_kana = 0
        for char in jp_word:
            if is_kana(char):
                n_kana += 1
        if n_kana / len(jp_word) > kana_limit:
            filter_out = True

        if len(kk_word) > max_length:
            filter_out = True

        if not filter_out:
            japanese_words_filtered.append(jp_word)
            katakana_words_filtered.append(kk_word)

    if not duplicates_allowed:
        japanese_words_filtered, katakana_words_filtered = \
            remove_duplicates(japanese_words_filtered, katakana_words_filtered)

    return japanese_words_filtered, katakana_words_filtered


def remove_duplicates(seq1, seq2):
    """Removes values in two lists based on duplicates found in one of them.

    Parameters
    ----------
    seq1 : list
        List that is checked for duplicates. If a duplicate is found, the first
        instance is kept while all others are removed.
    seq2 : list
        List that has values removed based on duplicates in list 1. Must be
        same length as seq1.

    Returns
    -------
    unique1 : list
        seq1, but with duplicates removed.
    unique2 : list
        seq2, but with duplicates removed (based on duplicates in seq1).
    """
    unique1 = []
    unique2 = []
    for i, j in zip(seq1, seq2):
        if i not in unique1:
            unique1.append(i)
            unique2.append(j)

    return unique1, unique2


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
    # pylint: disable=invalid-name
    jp_word_dict_path = 'japanese/44492-japanese-words-latin-lines-removed.txt'
    outfile_path = 'outdict.txt'
    limit = 1000

    jp_word_list = load_dictionary(jp_word_dict_path)
    jp_word_list = initial_filter_words(jp_word_list, word_limit=limit)

    kk_word_list = convert_wordlist_to_katakana(jp_word_list)

    jp_word_list, kk_word_list = filter_words(jp_word_list, kk_word_list,
                                              kana_limit=0.9)

    create_dictionary_file(outfile_path, jp_word_list, kk_word_list)
