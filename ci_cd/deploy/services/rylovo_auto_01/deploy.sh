#!/bin/bash

# Устанавливаем переменные
TEMP_PATH="../../../../src/services/image-logging-service/temp"
DEST_LIBS_PATH="../../../../src/services/image-logging-service/temp/libs"
SOURCE_LIBS_PATH="../../../../src/libs/python"

# Копируем каталог libs в temp/libs
echo "Try to remove directory $DEST_LIBS_PATH..."
rm -rf $DEST_LIBS_PATH
echo "Try to create directory $DEST_LIBS_PATH..."
mkdir -p $DEST_LIBS_PATH
echo "Copy directory libs to $DEST_LIBS_PATH..."
cp -r $SOURCE_LIBS_PATH/* $DEST_LIBS_PATH

# Запуск docker-compose в фоновом режиме
echo "Starting docker-compose..."
docker-compose up --build -d

# Проверка на успешность запуска
if [ $? -eq 0 ]; then
   echo "docker-compose was successfully started"
else
   echo "docker-compose failed with error"
   exit 1
fi

# Remove unnecessary files and directories
echo "Remove unnecessary files and directories"
rm -rf $DEST_LIBS_PATH

# Stop script
echo "Script was successfully executed"