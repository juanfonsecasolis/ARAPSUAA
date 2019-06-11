#!/bin/bash

rm -r venvTest & mkdir venvTest
virtualenv --system-site-packages venvTest
source venvTest/bin/activate

apt-get -y install python-pyaudio

#mysql-connector-python==2.1.6
#mysql-utilities==1.6.4
#pygobject==3.26.1
#PyAudio==0.2.11
#pyliblzma==0.5.3
#pyodbc
#pysqlite==2.7.0

pip install --upgrade pip

pip install -r requirements.txt


