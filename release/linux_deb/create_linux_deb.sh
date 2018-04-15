#!/bin/bash

# Change working directory to script directory
cd "$(dirname "$0")"

# Set variables
SOURCE_DIR=R421A08_relay_control
USR_SHARE_DIR=${SOURCE_DIR}/usr/share
USR_BIN_DIR=${SOURCE_DIR}/usr/bin
TEMP_DIR=${USR_SHARE_DIR}/R421A08_relay_control
DEB_FILE=${SOURCE_DIR}.deb

echo "Creating directory..."
mkdir -p $TEMP_DIR
cp -r $INPUT_DIR/* $TEMP_DIR

echo "Creating links..."
mkdir $USR_BIN_DIR
ln -s /usr/share/R421A08_relay_control/modbus $USR_BIN_DIR/modbus
ln -s /usr/share/R421A08_relay_control/relay $USR_BIN_DIR/relay
ln -s /usr/share/R421A08_relay_control/relay_gui $USR_BIN_DIR/relay_gui

echo "Building .deb file..."
dpkg-deb --build R421A08_relay_control

echo "Copy result file to output directory..."
mv ${DEB_FILE} ${OUTPUT_DIR}/${SOURCE_DIR}_${VERSION}_linux.deb

echo "Cleanup..."
rm -rf ${TEMP_DIR}
rm -rf $USR_BIN_DIR

echo ".deb file created."

