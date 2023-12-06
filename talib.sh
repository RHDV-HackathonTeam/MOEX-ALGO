#!/bin/bash

echo "wget ta-lib"
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzvf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
echo "build ta-lib"
make
echo "install ta-lib"
sudo make install
export TA_LIBRARY_PATH=$PREFIX/lib
export TA_INCLUDE_PATH=$PREFIX/include
