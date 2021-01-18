# KameKurosuPuzzleGeneration
Automatically build Japanese crossword puzzles for KameKurosu app. Requires クロスワード　ギバー software.

## Steps
1. Use ZKanji software to export a word list (I created a list using all JLPT kanji with JLPT levels annotated for each word)
2. Use preprocess_zkanji_wordlist.py to parse this ZKanji word list into lists which can be fed to クロスワード　ギバー software. This file also pickles the final word list which can be input into build_jlpt_graph.py to look at JLPT level vs frequency.
3. Open up クロスワード　ギバー, set input file and row/column numbers and save a file in the directory you want to save automatically generated crosswords into.
4. Delete that file so the automated software doesn't have to worry about overwrite popups.
5. Start up simulate_xword_generation.py. You then have 5 seconds to bring クロスワード　ギバー into focus.
6. It will then automatically generate and save crosswords into the directory.
7. Once complete, there will probably be some crosswords that did not generate (due to timeouts). Manually generate these. Typically 80%-90% of the requested number of crosswords will be generated automatically using default timeout (roughly 15s).
8. Run count_unique_words.py to see how many words are covered by the crosswords generated, as well as to make sure no duplicate crosswords were generated.
