#!/bin/bash

# Change working directory to script directory
cd "$(dirname "$0")"

# Set variables
FILENAME=R421A08_relay_control_${VERSION}_linux
FILE_PATH=${FILENAME}.tar.bz2

echo "Creating source directory..."
mkdir ${FILENAME}
cp -r ${INPUT_DIR}/* ${FILENAME}

echo "Creating tar.gz2..."
tar -pcjf ${FILE_PATH} ${FILENAME}

echo "Cleanup..."
rm -rf ${FILENAME}

mv ${FILE_PATH} ${OUTPUT_DIR}/

echo ".tar.gz2 file created."

