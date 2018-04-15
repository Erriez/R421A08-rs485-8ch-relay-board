#!/bin/bash

# Change working directory to script directory
cd "$(dirname "$0")"

# Set variables
TEMP_DIR=AppDir/usr/bin

echo "Downloading AppImage tools..."
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    wget -c "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod a+x appimagetool-x86_64.AppImage
fi

echo "Copy sources..."
echo ${INPUT_DIR}
echo ${TEMP_DIR}

cp -r ${INPUT_DIR} ${TEMP_DIR}

echo "Creating AppImage..."
ARCH=x86_64 ./appimagetool-x86_64.AppImage AppDir

# Move generated file to output directory
mv R421A08_Relay_Control-${VERSION}-x86_64.AppImage ${OUTPUT_DIR}/R421A08_relay_control_${VERSION}_linux-x86_64.AppImage

# Remove temp dir
rm -rf ${TEMP_DIR}

echo "AppImage created."

