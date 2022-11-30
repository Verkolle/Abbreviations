import re

# Necessary files for processing sentences.
fullforms = "text/abbreviation_fullforms.txt"
infile = "text/tagged.txt"
output = "text/throwaway.txt"
# Stores pairs of [fullform, abbreviation]
ff_contractions = []


def split_sentence(sentence, check, fout):
    ff = " " + check[0].lower()
    abbrev = " " + check[1].lower()

    ff_regex = re.compile("{}(?![a-zA-ZāčēģīķļņšūžĀČĒĢĪĶĻŅŠŪŽ])".format(ff))
    s = re.split(ff_regex, sentence)

    # Splitting as such is much faster, but doesn't take into account abbrevs followed by punctuation.
    # s = sentence.split(ff+" ")

    if len(s) > 1:
        for i in range(len(s) - 1):
            new_sentence = ff.join(s[:i+1]) + abbrev + ff.join(s[i+1:])
            if sentence[-2:] != ".." and new_sentence[-2:] == "..":
                new_sentence = new_sentence[:-1]
            fout.write(new_sentence + "\n")


def split_lemmatized(sentence, lemmatized, check, fout):
    s = lemmatized.split(" " + check + " ")
    new_sentence = ""

    for i in range(len(s)):
        if i == 0:
            new_sentence += s[i]


# This function is for SIMPLIFIED substitution of full forms
def simple_substitute(sentence_text, sentence_tagged, fout):
    # TODO: Rework substitution function
    # 1. Take into account lemma not just the sentence text
    # DONE: 2. Work with fullforms followed (preceded by) punctuation marks.
    # DONE: 3. The current version always substitutes all occurrences of a single abbrev. these should be separated
    # DONE: 4. Check if multiple possible abbrev. for the same full form are both shown.
    # DONE: 5. If contracted abbreviation is last word in a sentence ending with a dot, remove duplicate dot.
    # 6. Keep existing case consistent between full-form and abbrev.
    # 7. Merge lemmas for masculine and feminine words
    # 8. Output sentences with multiple abbreviations (ESPECIALLY if they're adjacent to each other)

    sentence_text_lemmatized = ""
    for word in sentence_tagged:
        sentence_text_lemmatized += word.split("\t")[2]

    # Checks by bruteforce any clear fullforms and substitutes them with abbreviations.
    # The modified sentences are put in "text/throwaway.txt"
    for check in ff_contractions:
        split_sentence(sentence_text, check, fout)


# Reads the infile passed as argument.
# For each sentence in the infile prints out all SIMPLE substituted sentences in outfile
def read_file(file):
    with open(file, "r", encoding="utf-8") as text_file:
        with open(output, "w", encoding="utf-8") as fout:
            text = text_file.read()
            # Split infile text by sentence
            sentences = text.split("\n\n")
            for x in sentences:
                # Split off each metadata/word line
                lines = x.split("\n")
                for line in lines:
                    # Pass the sentence text to SIMPLIFIED substitution.
                    sentence_text = ""
                    sentence_tagged = []
                    if line[0:6] == "# text":
                        sentence_text = line[9:]
                    elif line and line[0] != "#":
                        sentence_tagged.append(line)
                    simple_substitute(sentence_text, sentence_tagged, fout)
    return


# Loads the text files for processing
def load_texts():
    # Change input files here
    inputfiles = [infile]
    # Load the content of all input files
    for x in inputfiles:
        read_file(x)
    return


# Read all the fullforms and their corresponding abbreviations into a list for use in substitution
def load_fullforms():
    with open(fullforms, "r", encoding="utf-8") as fullform_file:
        for line in fullform_file:
            # Take each abbreviation entry
            line = line.strip()
            entry = line.split("\t")
            abbrev = entry[0]
            # For each fullform create an entry of structure [fullform, abbrev] in the main list
            if len(entry) > 1:
                for x in entry[1:]:
                    ff_contractions.append([x, abbrev])
    return


# Main find fullforms function call.
def find_fullforms():
    load_fullforms()
    load_texts()
    return
