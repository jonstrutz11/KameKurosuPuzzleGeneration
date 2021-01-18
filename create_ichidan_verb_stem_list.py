
from convert_to_dict import load_dictionary, is_kana
from jamdict import Jamdict

jp_word_dict_path = 'japanese/44492-japanese-words-latin-lines-removed.txt'
outfile_path = 'ichidan_verb_stems.txt'

jp_word_list = load_dictionary(jp_word_dict_path)

ichidan_verb_stem_list = []

jmd = Jamdict()

for i, word in enumerate(jp_word_list):
    if not i % 500:
        print(i, 'words processed.')

    ichidan = False

    # Make sure it starts with kanji and ends with kana
    # and is not an い-adjective
    if not is_kana(word[0]) and word[-1] != 'い' and is_kana(word[-1]):
        potential_ichidan_verb = word + 'る'

        result = jmd.lookup(potential_ichidan_verb)

        if result.entries:
            for entry in result.entries:
                if 'Ichidan' in str(entry) or 'ichidan' in str(entry):
                    ichidan = True
                    break
    if ichidan:
        ichidan_verb_stem_list.append(word)

with open(outfile_path, 'w', encoding='utf-8') as outfile:
    for ichidan_verb_stem in ichidan_verb_stem_list:
        outfile.write(ichidan_verb_stem)
        outfile.write('\n')
