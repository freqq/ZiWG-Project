#!/usr/bin/env python3

import glob
import os
import re
import time 
import pandas as pd

CSV_TO_CLAN_FILES_PATH = "../data/to_clean/*.csv"
RESULT_CSV_FILES_PATH = "../data/csv/"
CHARS_TO_REMOVE = re.compile(r'[\n\"\'/(){}\[\]\[]|@,.;:"#]')


def main():
    files = glob.glob(CSV_TO_CLAN_FILES_PATH)
    for file in files:
        start_file_time = time.time()
        print('Processing file: ' + os.path.basename(file))
        clean_file(file)
        print_file_summary(start_file_time)


def clean_file(file):
    # Read file into pandas DataFrame
    data_file = pd.read_csv(file)
    df = pd.DataFrame(data=data_file)

    # Clean data
    for index, row in df.iterrows():
        df.at[index,'title'] = clean_string(row['title'])

    # Save final DataFrame to CSV
    df.to_csv(path_or_buf=RESULT_CSV_FILES_PATH + os.path.basename(file).split('.')[0] + ".csv")


def print_file_summary(start_file_time):
    print('......................')
    end_file_time = time.time() - start_file_time
    print("Finished cleaning file in : ", end_file_time)
    print('----------------------')

def clean_string(string):
    string = string.lower()
    string = remove_stop_words(string)
    string = clean_marks(string)
    string = remove_unwanted_characters(string)
    string = remove_multiple_spaces(string)

    return string


def remove_unwanted_characters(text):
    return re.sub(CHARS_TO_REMOVE, '', text)


def remove_multiple_spaces(text):
    return re.sub(' +', ' ', text)


def clean_marks(element, is_author=False):
    """ Clean records from punctuation marks

    :param element:
    :param is_author:
    :return:
    """
    if element is not None and element.strip():
        element = element.strip()

        for character in [',', ';', ':', '/']:
            if element[-1] == character:
                return element[:-1].strip()

        if not is_author and element[-1] == '.':
            # don't strip trailing periods from author names
            return element[:-1].strip()

        return element.strip()

    return None


def remove_stop_words(element):
    return ' '.join([word for word in element.split() if word not in get_stop_words()])


def get_stop_words():
    with open("../data/stop_words.txt", 'r') as fh:
        return fh.read().splitlines()


if __name__ == '__main__':
    main()
