#!/bin/sh
cd example
rm *.class
javac *.java
cd ..
./run_unittest.py
