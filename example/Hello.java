package com.gkbrk.JVMTest;

import com.gkbrk.JVMTest.TestImport;

class Hello {
    public static final String greeting = "Hi";

    public static void main(String[] args) {
        TestImport.runA();
        TestImport.runA();
        TestImport.runA();
        TestImport.runA();
        TestImport.runA();
        TestImport t = new TestImport();
        for (int i = 0; i < 5; i++) {
            System.out.println("Test " + i);
        }
        t.test();
        t.test();
        t.test();
    }

    public static int addNumbers(int a, int b) {
        return a + b;
    }

    public static int subtractNum(int a, int b) {
        for (int i = 0; i < b; i++) {
            a--;
        }

        return a;
    }

    public static int addOne(int a) {
        return addNumbers(a, 1);
    }
}