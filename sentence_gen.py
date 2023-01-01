# sentence_gen.py
# # Autors: Viesturs Jūlijs Lasmanis
# Galvenais fails teikumu apstrādāšanai priekš mašīnmācīšanas.

import os
from os import listdir
from os.path import isfile, join
from pprint import pprint
import subprocess
import linecache

# LVTagger ielāde un palaišanas nosacījumi.
# Te LVTagger JAR fails ir pašlaik pārsaukts par tagger.jar
tagger_name = "assets/tagger_2.1.0.jar"
java_call = "java -mx1200m -jar {} -Dfile.encoding=UTF8".format(tagger_name)
# Ievad/Izvad-failu nosaukumi
midput_file = "text/owo.txt"
output_file = "text/tagged.txt"


# Izsaucam LVTagger padotajam ievadfailam "input_file".
# LVTagger sākumā izprintē kkādu nesakarīgu tekstu, to nodzēšam
def sentence_gen(input_file):

    subprocess.call("{} < {} > {}".format(java_call, input_file, midput_file), shell=True)
    with open(midput_file, "r", encoding="utf-8") as file_input:
        with open(output_file, "w", encoding="utf-8") as output:

            # Atstāj tikai marķētos teikumus.
            # Tos atpazīst pēc tā, ka conll marķējumā pirmais vienmēr ir ID, kas ir skaitlis.
            it = 0
            for line in file_input:
                if line[0] != "\t":
                    if line[0:2] == "1\t":
                        sentence = linecache.getline(input_file, it+1)
                        output.write("# sent_id = test-{}\n".format(it))
                        output.write("# text = {}".format(sentence))
                        it += 1
                    output.write(line)
    return
