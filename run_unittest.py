#!/usr/bin/env python3
import unittest
from pyjvm.Machine import Machine
from pyjvm.jstdlib.StdlibLoader import load_stdlib_classes

class JVMTest(unittest.TestCase):
    def setUp(self):
        self.jvm = Machine()
        load_stdlib_classes(self.jvm)
        self.jvm.load_class_file('example/IntegerTest.class')

    def test_return_0(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/IntegerTest/return0'), 0)

    def test_return_1(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/IntegerTest/return1'), 1)

    def test_return_5000(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/IntegerTest/return5000'), 5000)

    def test_passthrough(self):
        for i in range(500):
            self.assertEqual(self.jvm
                .call_function('jvmtest/IntegerTest/passthrough', i), i)

    def test_passthrough_loop(self):
        for i in range(500, 550):
            self.assertEqual(self.jvm
                .call_function('jvmtest/IntegerTest/passthrough_loop', i), i)

    def test_double(self):
        for i in range(500):
            self.assertEqual(self.jvm
                .call_function('jvmtest/IntegerTest/doubleNum', i), i * 2)

    def test_power(self):
        for i in range(500):
            self.assertEqual(self.jvm
                .call_function('jvmtest/IntegerTest/power', i), i * i)

if __name__ == '__main__':
    unittest.main()