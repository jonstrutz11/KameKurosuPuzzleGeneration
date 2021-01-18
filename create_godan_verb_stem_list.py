
from convert_to_dict import load_dictionary, is_kana
from jamdict import Jamdict

jp_word_dict_path = 'japanese/44492-japanese-words-latin-lines-removed.txt'
outfile_path = 'godan_verb_stems.txt'

jp_word_list = load_dictionary(jp_word_dict_path)

godan_verb_stem_list = []
godan_verb_dictform_list = []

jmd = Jamdict()

endings = 'うつすくむるぶぐぬ'

for i, word in enumerate(jp_word_list):
    if not i % 500:
        print(i, 'words processed.')

    # Make sure it starts with kanji and ends with kana
    # and is not an い-adjective
    if not is_kana(word[0]):
        possible_godan = True
        if word.endswith('っ'):
            endings = 'うつる'
        elif word.endswith('ん'):
            endings = 'むぬぶ'
        elif word.endswith('い'):
            endings = 'くぐ'
        elif word.endswith('し'):
            endings = 'す'
        else:
            possible_godan = False

        if possible_godan:
            godan = False
            for ending in endings:
                possible_godan_verb = word[:-1] + ending

                result = jmd.lookup(possible_godan_verb)

                if result.entries:
                    for entry in result.entries:
                        if 'Godan' in str(entry) or 'godan' in str(entry):
                            godan = True
                if godan:
                    godan_verb_stem_list.append(word)
                    godan_verb_dictform_list.append(possible_godan_verb)
                    print(word, possible_godan_verb)
                    break

with open(outfile_path, 'w', encoding='utf-8') as outfile:
    for stem, dict_form in zip(godan_verb_stem_list, godan_verb_dictform_list):
        outfile.write(stem + ',' + dict_form)
        outfile.write('\n')
