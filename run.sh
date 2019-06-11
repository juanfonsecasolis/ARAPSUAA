#!/bin/bash
export PYTHONPATH="$PWD/src"
#cd src
python2.7 src/tests/TestFigures.py
python2.7 src/tests/TestBatchFigures.py
pthon2.7 src/tests/TestOctave.py
python2.7 src/tests/TestScenarios.py
#python2.7 src/tests/TestBruteForce.py
#cp -r /tmp/outputDataAPS ~/outputDataAPS
