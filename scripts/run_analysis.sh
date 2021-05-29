#!/bin/bash

source logger.sh

set -eE

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function convert_marc_to_csv() {
    cd ${SOURCE_DIR}/../tools
    python convert.py
    cd scripts
}

function remove_identical_duplicates() {
    cd ${SOURCE_DIR}/../tools
    python remove_identical_duplicates.py
    cd scripts
}

function main() {
    log_info "Starting analysis."

    convert_marc_to_csv
    remove_identical_duplicates

    log_info "Analysis finished"
}

main