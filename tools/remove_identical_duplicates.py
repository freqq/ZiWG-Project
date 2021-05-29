#!/usr/bin/env python3

import glob
import os

import pandas as pd

CSV_FILES_PATH = "../data/csv/*.csv"

def main():
    files = glob.glob(CSV_FILES_PATH)
    for file in files:
        print('Processing file: ' + os.path.basename(file))
        data_file = pd.read_csv(file)
        df = pd.DataFrame(data=data_file)
        df = df.drop_duplicates()
        df.to_csv("../data/removed_duplicates/" + os.path.basename(file))

if __name__ == '__main__':
    main()
