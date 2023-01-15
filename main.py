from acro_list import *
from sentence_gen import *
from find_fullforms import *
from split_data import *

# File structure:
# main.py
#   -acro_list
#     --cut_defs
#   -sentence_gen
#   -find_fullforms
#     --split_data

input_file = "text/uwu.txt"


# Pavaicājam lietotājam, kuras funkcijas vēlas izpildīt.
def user_prompt(text):
    question = input("Do you wish to {}?".format(text))
    if question == "Y":
        return True
    return False


# The main function call in the code.
def main():
    # Iegūstam pilnu sarakstu ar abbreviatūrām un to atšifrējumiem.
    if user_prompt("recompile the list of abbreviation full forms"):
        create_acro_list()
    # Korpusa tekstu pārveidojam ar LVTagger palīdzību par marķētu tekstu.
    if user_prompt("generate tagged text from input files"):
        sentence_gen(input_file)
    # Mēģināsim nolasīt abbreviatūru atšifrējumus iekš marķēta teksta.
    if user_prompt("find and replace full forms in text with respective abbreviations"):
        find_fullforms()
        split_data()


if __name__ == "__main__":
    main()
