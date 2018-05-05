#/bin/bash
#MUST BE RUN AS ROOT
echo "Installing dependencies"
apt-get update
apt-get -y install python3-rpi.gpio python-dev build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libsdl1.2-dev python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev

echo "Installing Python 3.6.5"
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
./configure
make
make altinstall

echo "Upgrading pip3.6"
pip3.6 install --upgrade pip

echo "Installing RPi.GPIO"
pip3.6 install RPi.GPIO

echo "Installing pygame"
pip3.6 install pygame

echo "Installing numpy"
pip3.6 install numpy

echo "Installing websockets"
pip3.6 install websockets

echo "Cleaning up"
apt-get -y autoremove
apt-get -y clean