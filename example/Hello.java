package com.gkbrk.JVMTest;

import com.gkbrk.JVMTest.TestImport;

class Hello {
    public static final String greeting = "Hi";

    public static void main(String[] args) {
        addNumbers(3, 4);
    }

    public static int addNumbers(int a, int b) {
        for (int i = 0; i < b; i++) {
            a++;
        }

        return a;
    }

    public static int subtractNum(int a, int b) {
        for (int i = 0; i < b; i++) {
            a--;
        }

        return a;
    }
}