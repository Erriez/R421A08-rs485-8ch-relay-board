#!/bin/bash

# Absolute path to this script including filename
SCRIPTPATH=$(readlink -f "$0")
# Get path to this script
BASEDIR=$(dirname ${SCRIPTPATH})
# Go to this script directory
cd ${BASEDIR}

# Export variables to other scripts
export VERSION="v1.0.1"
export OUTPUT_DIR=${BASEDIR}/build
export INPUT_DIR=${BASEDIR}/build/exe.linux-x86_64-3.5

# Remove existing output directory
if [ -d ${OUTPUT_DIR} ]; then
    rm -rf ${OUTPUT_DIR}
fi

# Create output directory
mkdir ${OUTPUT_DIR}

# Activate virtualenv
source ../venv/bin/activate

# Build Linux executables
python setup.py build

# Create tar.bz2
linux_tar_bz2/create_linux_tar.bz2.sh

# Create AppImage
linux_appimage/create_linux_appimage.sh

# Create .deb
linux_deb/create_linux_deb.sh

echo "See build/ directory with generated binaries."
