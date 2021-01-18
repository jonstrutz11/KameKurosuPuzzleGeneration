"""Test our pykakasi module."""

import pykakasi


DICT_PATH = 'japanese/44492-japanese-words-latin-lines-removed.txt'

kks = pykakasi.kakasi()
kks.setMode('J', 'K')
kanji_conv = kks.getConverter()
kks.setMode('H', 'K')
hiragana_conv = kks.getConverter()


with open(DICT_PATH, 'r', encoding='utf-8') as infile:
    all_words = infile.readlines()
    filtered_words = [word.rstrip() for word in all_words
                      if len(word.rstrip()) > 1]
    filtered_words = filtered_words[30:40]

for word in filtered_words:
    print(word)
    katakana = hiragana_conv.do(kanji_conv.do(word))
    print(katakana, '\n\n')
