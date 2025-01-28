#!/bin/bash

echo "Script was ran under user: $USER"

set -e

# Готовим переменные окружения
export HOST_SRC_PATH=$(pwd)/../../../src
export HOST_TESTS_PATH=$(pwd)/../../../tests

# Устанавливаем переменные
SOURCE_LIBS_PATH="$HOST_SRC_PATH/libs/python"

services=(
    "$HOST_SRC_PATH/services/image-logging-service/temp"
    "$HOST_SRC_PATH/services/video-capture-service/temp"
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

# Создаем временный каталог для контейнера
echo "Try to remove directory /tmp/tests"
rm -rf /tmp/tests
echo "Try to create directory /tmp/tests"
mkdir /tmp/tests
chmod -R 777 /tmp/tests

# Построение образа
echo ">>> Building Docker image..."
docker-compose build

# Запуск тестов
echo ">>> Running tests..."
docker-compose run --rm test-runner

# Удаление остановленных контейнеров и зависимостей
echo ">>> Cleaning up..."
docker-compose down