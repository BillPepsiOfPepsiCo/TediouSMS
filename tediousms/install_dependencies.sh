#/bin/bash
#MUST BE RUN AS ROOT
echo "Installing dependencies"
apt-get update
apt-get -y install python3-rpi.gpio
apt-get -y install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev

echo "Installing Python 3.6.5"
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
./configure
make
make altinstall

echo "Cleaning up"
rm -r Python-3.6.5
rm Python-3.6.5.tar.xz
apt-get -y --purge remove build-essential tk-dev
apt-get -y --purge remove libncurses5-dev libncursesw5-dev libreadline6-dev
apt-get -y --purge remove libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
apt-get -y --purge remove libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
apt-get -y autoremove
apt-get -y clean

echo "Upgrading pip3.6"
pip3.6 install --upgrade pip

echo "Installing RPi.GPIO"
pip3.6 install RPi.GPIO

echo "Installing websockets"
pip3.6 install websockets
