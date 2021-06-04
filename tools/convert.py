#!/usr/bin/env python3
"""
Base code for this script was taken from https://github.com/DavidChouinard/mrc_to_csv
Code was modified to make it work with python3
"""
import csv
import os
import re

from pymarc import MARCReader

CHARS_TO_REMOVE = re.compile(r'[\n\"\'/(){}\[\]\[]|@,.;:"#]')
MAX_ENTRIES_TO_READ = 5200000


def main():
    """ Main function
    """
    for filename in os.listdir('../data/mrc/'):
        if os.path.isdir('data/mrc/' + filename) or filename[0] == '.':
            continue

        with open('../data/csv/' + os.path.splitext(filename)[0] + '.csv', 'w') as input_file, \
                open('../data/mrc/' + filename, 'rb') as output_file:

            reader = MARCReader(output_file)
            writer = csv.writer(input_file)
            writer.writerow(['isbn', 'title', 'author',
                             'publisher', 'pub_place', 'pub_year',
                             'extent', 'dimensions', 'subject', 'inclusion_date',
                             'source', 'library', 'notes'])

            for i, record in enumerate(reader):
                if i <= MAX_ENTRIES_TO_READ:
                    pub_place = clean_marks(record['260']['a']) if '260' in record else None
                    extent = clean_marks(record['300']['a'], True) if '300' in record else None
                    dimensions = record['300']['c'] if '300' in record else None
                    subject = record['650']['a'] if '650' in record else None
                    inclusion_date = record['988']['a'] if '988' in record else None
                    source = record['906']['a'] if '906' in record else None
                    library = record['690']['5'] if '690' in record else None

                    notes = " ".join([field['a'] for field in record.notes() if 'a' in field])

                    writer.writerow([record.isbn(), clean_title(record.title()), clean_marks(record.author(), True),
                                    clean_marks(record.publisher()), pub_place, clean_marks(record.pubyear()),
                                    extent, dimensions, subject, inclusion_date,
                                    source, library, notes])

                    if i % 100 == 0:
                        print('Processed ' + str(i) + ' records.')


def clean_title(title):
    title = title.lower()
    title = remove_stop_words(title)
    title = clean_marks(title)
    title = remove_unwanted_characters(title)
    title = remove_multiple_spaces(title)

    return title


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
