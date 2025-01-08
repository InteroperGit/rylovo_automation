#!/bin/bash

# Устанавливаем переменные
SOURCE_LIBS_PATH="../../../../src/libs/python"

services=(
    "../../../../src/services/image-logging-service/temp"
    "../../../../src/services/video-capture-service/temp"
)

for TEMP_PATH in "${services[@]}"; do
   DEST_LIBS_PATH="$TEMP_PATH/libs"

   # create temporary directory
   echo "Try to remove directory $TEMP_PATH..."
   rm -rf $TEMP_PATH
   echo "Try to create directory $TEMP_PATH..."
   mkdir -p $TEMP_PATH
   # create dest directory
   echo "Try to remove directory $DEST_LIBS_PATH..."
   rm -rf $DEST_LIBS_PATH
   echo "Try to create directory $DEST_LIBS_PATH..."
   mkdir -p $DEST_LIBS_PATH
   echo "Copy directory libs to $DEST_LIBS_PATH..."
   cp -r $SOURCE_LIBS_PATH/* $DEST_LIBS_PATH
done

# Запуск docker-compose в фоновом режиме
echo "Starting docker-compose..."
docker-compose up --build -d

# Checking for success of starting docker-compose
if [ $? -eq 0 ]; then
   echo "docker-compose was successfully started"
else
   echo "docker-compose failed with error"
   exit 1
fi

# Remove unnecessary files and directories
for TEMP_PATH in "${services[@]}"; do
   echo "Remove unnecessary files and directories"
   rm -rf $TEMP_PATH
done

# Stop script
echo "Script was successfully executed"