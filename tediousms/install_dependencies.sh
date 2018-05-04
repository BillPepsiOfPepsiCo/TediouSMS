#/bin/bash
#MUST BE RUN AS ROOT
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
tar xzvf Python-3.6.0.tgz
cd Python-3.6.0/
./configure --with-tcltk-includes='-I/opt/ActiveTcl-8.5/include' --with-tcltk-libs='/opt/ActiveTcl-8.5/lib/libtcl8.5.so /opt/ActiveTcl-8.5/lib/libtk8.5.so'
make -j4
make install
pip3 install websockets