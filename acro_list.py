import re
import xml.etree.ElementTree as ET
from cut_defs import *

# ----------------------------------
# Used resources
definitions = "assets/definitions.xml"
entries = "assets/entries.txt"
# ----------------------------------
# Data organization files
abbreviation_full_forms = "text/abbreviation_fullforms.txt"


def flatten(li):
    return [item for sublist in li for item in sublist]


# Iegūstam visas realizācijas kādam vārdnīcas vārdam.
def acronym_full_forms(entry, xml_root):
    definition_texts = []
    definition_texts.clear()

    test = r"^tezaurs\/" + re.escape(entry) + "(:[0-9])?$"
    id_pattern = re.compile(test)
    for x in xml_root[1]:
        if id_pattern.match(x.attrib.get("id")):
            for y in x:
                tag = y.tag
                if y.tag[0] == "{":
                    tag = y.tag.split("}")[1]
                if tag == "sense":
                    definition_texts.append(cut_def(entry, y[0].text))
    definition_texts = flatten(definition_texts)
    return definition_texts


def create_acro_list():
    acronym_pattern = re.compile("^([a-zA-ZāčēģīķļņšūžĀČĒĢĪĶĻŅŠŪŽ]+\. ?){1,}$")
    # Clear and open output file.
    open(abbreviation_full_forms, "w").close()
    fout = open(abbreviation_full_forms, "a", encoding="utf-8")
    # Open file for definitions.
    tree = ET.parse(definitions)
    xml_root = tree.getroot()
    # Read all the words in tezaurs that are from acronym dictionaries "i1" or "i2"
    with open(entries, "r", encoding="utf-8") as fin:
        # Read the entries file
        # 8-th position stores list of dictionaries for each word
        # 0-th position stores lemma
        for line in fin:
            line = line.strip()
            entry = line.split("\t")
            dicts = entry[8]
            # dict_list = dicts.split(",")

            word = entry[0]
            # Check if word belongs to either "i1" or "i2".
            # Check if word matches pattern for typical acronyms in all dictionaries.
            # if any(x in dict_list for x in ["i1", "i2"]) or acronym_pattern.match(word):
            if acronym_pattern.match(word):
                word = entry[0]
                ff = acronym_full_forms(word, xml_root)
                print(word, end='')
                for g in ff:
                    print("\t" + g, end='')
                print("")
                fout.write(word)
                for g in ff:
                    fout.write("\t" + g)
                fout.write("\n")
                continue

    fin.close()
    fout.close()
    return
