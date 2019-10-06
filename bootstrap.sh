#!/bin/sh

cd /
mkdir /cross_tools
cd /cross_tools

wget -O - http://musl.cc/x86_64-linux-musl-native.tgz | tar -xzf -
wget -O - http://musl.cc/aarch64-linux-musl-native.tgz | tar -xzf -
wget -O - http://musl.cc/aarch64-linux-musl-cross.tgz | tar -xzf - 
