package com.gkbrk.JVMTest;

import com.gkbrk.JVMTest.TestImport;

class Hello {
    public static final String greeting = "Hi";

    public static void main(String[] args) {
        int a = 46462;
        int b = 8;
        System.out.println("Hello, World!");
        System.out.println(addNumbers(a, b));
    }

    public static int addNumbers(int a, int b) {
        return a + b;
    }
}