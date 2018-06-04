package com.gkbrk.JVMTest;

class TestImport {
    public int t;
    public static int a = 0;

    public TestImport() {
        System.out.println("TestImport initialized");
        t = 500;
    }

    public void test() {
        System.out.println(t);
        t++;
    }

    public static void runA() {
        System.out.println(a);
        a++;
    }

    public static int getBestNumber() {
        return 4;
    }
}