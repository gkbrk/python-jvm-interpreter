package jvmtest;

class IntegerTest {
    public static int return0() {
        return 0;
    }

    public static int return1() {
        return 1;
    }

    public static int return5000() {
        return 5000;
    }

    public static int passthrough(int a) {
        return a;
    }

    public static int passthrough_loop(int a) {
        int b = 0;
        for (int i = 0; i < a; i++) {
            b++;
        }
        return b;
    }

    public static int doubleNum(int a) {
        return a * 2;
    }

    public static int power(int a) {
        return a * a;
    }
}