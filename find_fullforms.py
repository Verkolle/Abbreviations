import re
from os import listdir
from os.path import isfile, join

# Necessary files for processing sentences.
fullforms = "text/abbreviation_fullforms.txt"

infile = "text/tagged.txt"
output = "text/output.txt"

# Files for storing NN training & evaluation data pairs
nn_input = "text/nn_input.txt"
nn_output = "text/nn_output.txt"

# Stores pairs of [fullform, abbreviation]
ff_contractions = []


def x_in_y(query, base):
    try:
        l = len(query)
    except TypeError:
        l = 1
        query = type(base)((query,))

    for i in range(len(base)):
        if base[i:i+l] == query:
            return i, l
    return False, False


def split_sentence(sentence, check, fout):
    ff = " " + check[0].lower()
    abbrev = " " + check[1].lower()

    # Check if fullforms found are not a full word, and are not cut out of the beginning of one
    ff_regex = re.compile("{}(?![a-zA-ZāčēģīķļņšūžĀČĒĢĪĶĻŅŠŪŽ])".format(ff))
    s = re.split(ff_regex, sentence)

    # Splitting as follows is much faster, but doesn't take into account abbrevs followed by punctuation.
    # ff = " " + check[0].lower() + " "
    # s = sentence.split(" " + check[0].lower())

    if len(s) > 1:
        for i in range(len(s) - 1):
            new_sentence = ff.join(s[:i+1]) + abbrev + ff.join(s[i+1:])
            # If contracted abbreviation is last word in a sentence ending with a dot, remove duplicate dot.
            if sentence[-2:] != ".." and new_sentence[-2:] == "..":
                new_sentence = new_sentence[:-1]
            fout.write(new_sentence + "\n")


def split_lemmatized(sentence, tagged, check, fout):
    ff = check[0].lower().split(" ")    # [b, c]
    abbrev = check[1].lower()           # d

    delemma = [[],[]]                   # [[au, ba, ce, du], [a, b, c, d]]
    for word in tagged:
        data = word.split("\t")
        delemma[0].append(data[2])  # Lemmas
        delemma[1].append(data[1])  # Actual words

    a, b = x_in_y(ff, delemma[0])
    if a and b:
        if delemma[0][a:a+b] != delemma[1][a:a+b]:
            text_to_substitute = ' '.join(delemma[1][a:a+b]).lstrip()
            split_sentence(sentence, [text_to_substitute, abbrev], fout)


# This function is for substitution of full forms
def simple_substitute(sentence_text, sentence_tagged, fout):
    # DONE: 1. Take into account lemma not just the sentence text
    # DONE: 2. Work with fullforms followed (preceded by) punctuation marks.
    # DONE: 3. The current version always substitutes all occurrences of a single abbrev. these should be separated
    # DONE: 4. Check if multiple possible abbrev. for the same full form are both shown.
    # DONE: 5. If contracted abbreviation is last word in a sentence ending with a dot, remove duplicate dot.
    # TODO: 6. Keep existing case consistent between full-form and abbrev.
    # TODO: 7. Merge lemmas for masculine and feminine words
    # TODO: 8. Output sentences with multiple abbreviations (ESPECIALLY if they're adjacent to each other)
    #       Probably I can find abbrev clusters by checking if the string inbetween them is all whitespace
    #       A function for this is str.isspace()

    # Checks by bruteforce any clear fullforms and substitutes them with abbreviations.
    # The modified sentences are put in "text/throwaway.txt"
    for check in ff_contractions:
        split_sentence(sentence_text, check, fout)
        split_lemmatized(sentence_text, sentence_tagged, check, fout)


# Reads the infile passed as argument.
# For each sentence in the infile prints out all SIMPLE substituted sentences in outfile
def read_file(file):
    with open(file, "r", encoding="utf-8") as text_file:
        with open(output, "a", encoding="utf-8") as fout:
            text = text_file.read()
            # Split infile text by sentence
            sentences = text.split("\n\n")
            for x in sentences:
                # Split off each metadata/word line
                lines = x.split("\n")
                sentence_text = ""
                sentence_tagged = []
                for line in lines:
                    # Pass the sentence text to SIMPLIFIED substitution.
                    if line[0:6] == "# text":
                        sentence_text = line[9:]
                    elif line and line[0] != "#":
                        sentence_tagged.append(line)
                if sentence_text:
                    simple_substitute(sentence_text, sentence_tagged, fout)
    return


# Loads the text files for processing
def load_texts():
    # Change input files here
    mypath = "testing/conll"
    inputfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    open(output, 'w')
    # Load the content of all input files
    for x in inputfiles:
        print(x)
        read_file("testing/conll/"+x)
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
