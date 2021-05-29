#!/usr/bin/env python3

import glob
import os
import pandas as pd
import numpy as np
import time
import sparse_dot_topn.sparse_dot_topn as ct
import dataframe_image as dfi

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

REMOVED_DUPLICATES_CSV_FILES_PATH = "../data/removed_duplicates/*.csv"
RESULT_CSV_FILES_PATH = "../data/result/"
TFIDF_VECTORIZER = TfidfVectorizer(ngram_range=(1, 2), max_df=0.9, min_df=5, token_pattern=r'(\S+)')
SIMILARITY_SCORE = 'similairity_score'
MAX_SIMILARITY_SCORE = 0.9999
MIN_SIMILARITY_SCORE = 0.9


def main():
    files = glob.glob(REMOVED_DUPLICATES_CSV_FILES_PATH)
    for file in files:
        start_file_time = time.time()
        print('Processing file: ' + os.path.basename(file))
        analyze_file(file)
        print_file_summary(start_file_time)


def analyze_file(file):
    # Read files into pandas DataFrame
    data_file = pd.read_csv(file)
    df = pd.DataFrame(data=data_file)

    # Calculate transforming text to vectors
    start_time = time.time()
    tf_idf_matrix = TFIDF_VECTORIZER.fit_transform(df['title'])
    end_time = time.time() - start_time
    print("Finished transforming text to vectors in: ", end_time)

    # Calculate cosine similarity
    start_time = time.time()
    matches = cosine_similarity(tf_idf_matrix, tf_idf_matrix.transpose(), 10, 0.8)
    end_time = time.time() - start_time
    print("Finished cosine similarity calculation in: ", end_time)

    # Getting matches DataFrame
    start_time = time.time()
    matches_df = get_matches_df(matches, df['title'], df['isbn'], top=3000)
    end_time = time.time() - start_time
    print("Finished getting matches DataFrame in: ", end_time)

    # Remove all matches outside similarity threshold -> final DataFrame
    final_data_frame_min = matches_df[matches_df[SIMILARITY_SCORE] > MIN_SIMILARITY_SCORE]
    final_data_frame = final_data_frame_min[matches_df[SIMILARITY_SCORE] < MAX_SIMILARITY_SCORE]

    # Sort values in DataFrame by similarity_score
    sorted_final_df = final_data_frame.sort_values(by=SIMILARITY_SCORE, ascending=False)

    # Save final DataFrame to CSV
    sorted_final_df.to_csv(path_or_buf=RESULT_CSV_FILES_PATH + os.path.basename(file).split('.')[0] + ".csv")

    # Saving top 10 matches as png file
    top_10_matches = sorted_final_df.head(10)
    save_table_image(top_10_matches, os.path.basename(file).split('.')[0])


def print_file_summary(start_file_time):
    print('......................')
    end_file_time = time.time() - start_file_time
    print("Finished processing file in : ", end_file_time)
    print('----------------------')


def cosine_similarity(A, B, ntop, lower_bound=0):
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
    idx_dtype = np.int32
    nnz_max = M*ntop

    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)
    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)
    return csr_matrix((data, indices, indptr), shape=(M, N))


def get_matches_df(sparse_matrix, name_vector, isbn, top=100):
    non_zeros = sparse_matrix.nonzero()
    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]

    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size

    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)

    for index in range(0, nr_matches):
        left_side[index] = name_vector[sparserows[index]] + " ; " + get_isbn_value(isbn[sparserows[index]])
        right_side[index] = name_vector[sparsecols[index]] + " ; " + get_isbn_value(isbn[sparserows[index]])
        similairity[index] = sparse_matrix.data[index]

    return pd.DataFrame({'First entry (Title + ISBN)': left_side,
                        'Second entry (Title + ISBN)': right_side,
                         SIMILARITY_SCORE: similairity})


def get_isbn_value(isbn):
    return '-' if is_nan(isbn) else str(isbn)


def is_nan(string):
    return string != string


def save_table_image(data_frame, file_name):
    df_styled = data_frame.style.background_gradient()
    dfi.export(df_styled, "../data/png/" + file_name + ".png")


if __name__ == '__main__':
    main()
