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

    def test_iterative_fibonacci(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/IntegerTest/iterativeFibonacci', 20), 6765)

    def test_recursive_fibonacci(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/IntegerTest/recursiveFibonacci', 7), 13)

class StringTest(unittest.TestCase):
    def setUp(self):
        self.jvm = Machine()
        load_stdlib_classes(self.jvm)
        self.jvm.load_class_file('example/StringTest.class')

    def test_rot13_hello_world(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/StringTest/rot13', 'Hello World!')
                                                     , 'Uryyb Jbeyq!')

    def test_reverse_string(self):
        r = self.jvm.call_function('jvmtest/StringTest/reverseString', 'Test message!')
        self.assertEqual(r, '!egassem tseT')

class InstanceTest(unittest.TestCase):
    def setUp(self):
        self.jvm = Machine()
        load_stdlib_classes(self.jvm)
        self.jvm.load_class_file('example/InstanceTest.class')

    def test_single_instance(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/InstanceTest/test_single'), 12345)

    def test_multiple_instance_1(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/InstanceTest/test_multiple_1'), 12345)

    def test_multiple_instance_2(self):
        self.assertEqual(self.jvm
            .call_function('jvmtest/InstanceTest/test_multiple_2'), 54321)

class ArrayTest(unittest.TestCase):
    def setUp(self):
        self.jvm = Machine()
        load_stdlib_classes(self.jvm)
        self.jvm.load_class_file('example/ArrayTest.class')

    def test_insertion_sort(self):
        l = [4, 3, 5, 1]
        r = self.jvm.call_function('jvmtest/ArrayTest/insertionSort', l)
        self.assertEqual(r, None)
        self.assertEqual(l, [1, 3, 4, 5])

    def test_cocktail_sort(self):
        l = [4, 3, 5, 1]
        r = self.jvm.call_function('jvmtest/ArrayTest/cocktailSort', l)
        self.assertEqual(r, None)
        self.assertEqual(l, [1, 3, 4, 5])

    def test_sum(self):
        l = [5, 5, 14, 3]
        r = self.jvm.call_function('jvmtest/ArrayTest/sum', l)
        self.assertEqual(r, sum(l))

if __name__ == '__main__':
    unittest.main()
