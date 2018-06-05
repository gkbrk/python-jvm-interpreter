# JVM implementation in Python

_python-jvm-interpreter_ is an implementation of the Java Virtual Machine in
Python. It works by parsing and interpreting the Java Class files.

## Running the tests
In order to run the examples or unit tests, you need to compile the Java source
files into _.class_ files. To do this, you can use `javac`. In order to compile
all the files in the example folder, you can run `javac *.java`.

As more functionality is implemented, the amount of test cases should be
increased in order to make it easier to check if anything is broken.