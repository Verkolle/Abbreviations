import random

# Input files of all data set samples
nn_input = "text/nn_input.txt"
nn_output = "text/nn_output.txt"

# Training dataset
train_input = "text/datasets/train/train_input.txt"
train_output = "text/datasets/train/train_output.txt"

# Validation dataset
validate_input = "text/datasets/validate/validate_input.txt"
validate_output = "text/datasets/validate/validate_output.txt"

# Testing dataset
test_input = "text/datasets/test/test_input.txt"
test_output = "text/datasets/test/test_output.txt"

# Dataset split
train_set = 0.8
validation_set = 0.1
test_set = 0.1


def split_data():
    # Get line count in full set
    fp = open(nn_input, "r", encoding="utf-8")
    x = len(fp.readlines())-1
    fp.close()

    # Get 20% of lines for validation & test set.
    val_and_test = random.sample(range(1, x), round(x*(validation_set+test_set)))
    v = len(val_and_test)

    # Get 10% of lines for validation set
    validation_percentage = validation_set/(validation_set+test_set)
    validation_sentences = random.sample(range(1, v), round(v*(validation_percentage)))

    # Get 10% of lines for test set
    test_sentences = [x for x in val_and_test if x not in validation_sentences]

    # Get all the lines
    f_source = open(nn_input, "r", encoding="utf-8")
    source_lines = f_source.readlines()
    f_source.close()

    f_target = open(nn_output, "r", encoding="utf-8")
    target_lines = f_target.readlines()
    f_target.close()

    # Split all lines into files
    for i in range(1, x):
        if i in validation_sentences:
            f_input = open(validate_input, "a", encoding="utf-8")
            f_output = open(validate_output, "a", encoding="utf-8")
        elif i in test_sentences:
            f_input = open(test_input, "a", encoding="utf-8")
            f_output = open(test_output, "a", encoding="utf-8")
        else:
            f_input = open(train_input, "a", encoding="utf-8")
            f_output = open(train_output, "a", encoding="utf-8")

        f_input.write(source_lines[i-1])
        f_output.write(target_lines[i-1])