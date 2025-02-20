# Abbreviations
Working on normalizing abbreviations in Latvian

This is the repository for the project of Latvian text normalization task.
The python files within this directory are used for the creation of the dataset used for training the machine learning model.

There are additional folders for storing information:

 - "assets" includes information from external sources used for running the program. 
This includes "definitions.txt", "entries.txt" for the creation of the abbreviation list. 
Additionally, a version of "LVTagger" should be here if the user wants to generatee annotated sentences from simple sentences.
 - "testing" includes the folder "conll" where all CoNLL files used for sentence generation are stored."
 - "text" includes all the various text files generated by running the code.
 - "sockeye" is a seperate directory, which includes the necessary structure for running the model.

main.py is the main file, which is used to run all other processes.

The main file prompts 3 different processes (y/n) in the following order:
1. Creation of the abbreviation list file ("abbreviation_fullforms.txt") by calling "acro_list.py" and "cut_defs.py".
2. Creation of tagged sentences from unmarked sentences using LVTagger 2.1.0 (which should be included in "assets") by calling "sentence_gen.py". This code is not used in the final version of generating the data set as the FullStack corpus is used instead. However, this could possibly be used in the future.
3. Creation of data set ("find_fullforms.py") by using the FullStack CoNLL files in folder "testing/conll" and splitting the created data set into training, validation and test ("split_data.py")

The final stage for training the model is running the Sockeye framework on the resulting datasets. See the README file within the folder "sockeye" regarding the training process.
