#!/bin/bash

# Ensure we are in dependency directory
rm -rf build/dependency
mkdir -p build/dependency
cd build/dependency || exit

# Exclude plain jar.
JAR_FILE=$(find ../libs -name "*.jar" -a ! -name "*-plain.jar")

# Explode jar
jar -xf "$JAR_FILE"

# Build docker image
cd ../..
docker build --build-arg DEPENDENCY=build/dependency --build-arg PLUGINS=./plugins -t dockreg.el.nist.gov/e3/api:java .
