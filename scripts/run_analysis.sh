#!/bin/bash

source logger.sh

set -eE

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function convert_marc_to_csv() {
    log_info "-------------------------------------"
    log_info "Starting - Convert MARC to CSV."

    cd ${SOURCE_DIR}/../tools
    python convert.py
    cd ../scripts

    log_info "Finished - Convert MARC to CSV."
}

function transform_text_to_vectors_and_analyse() {
    log_info "-------------------------------------"
    log_info "Starting - Transform text to vectors and analyse."

    cd ${SOURCE_DIR}/../tools
    python transform_text_to_vectors.py
    cd ../scripts

    log_info "Finished - Transform text to vectors and analyse."
    log_info "-------------------------------------"
}

function main() {
    log_info "Starting analysis."

    convert_marc_to_csv
    transform_text_to_vectors_and_analyse

    log_info "------FINISH------"
    log_info "Analysis finished."
}

time main