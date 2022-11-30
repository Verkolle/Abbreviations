import re


# This function receives a string which is a single definition of an abbreviation.
def cut_def(entry, definition):
    # Get rid of text in brackets (including brackets)
    definition = re.sub("[\(].*?[\)]", "()", definition)

    # First we split the definition along semicolons.
    definition = definition.split(";")
    output = []
    output.clear()
    # ----------------------------------------------------------------
    # Process all of the definitions here.
    # ----------------------------------------------------------------
    # TODO: Finetune extraction of fullforms from definitions.
    for x in definition:
        x = x.split("(")[0]
        x = x.split(" - ")[0]
        x = x.split(", -a")[0]
        # x = x.split(" valoda")[0]
        if len(x) != 1:
            if x[0] == " ":
               x = x[1:]
            if x[-1] == " ":
                x = x[:-1]
            if x[-1] == ".":
                x = x[:-1]
            if x[-1] == "-":
                x = x[:-1]
            output.append(x)
    # ----------------------------------------------------------------
    # End of processing.
    # ----------------------------------------------------------------
    # Exit   
    return output