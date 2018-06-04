package com.gkbrk.JVMTest;

class TestImport {
    public int t;

    public TestImport() {
        System.out.println("TestImport initialized");
        t = 500;
    }

    public void test() {
        System.out.println(t);
        t++;
    }

    public static int getBestNumber() {
        return 4;
    }
}