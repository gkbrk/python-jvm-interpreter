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

    public static int recursiveFibonacci(int n) {
        return (n < 2) ? n : recursiveFibonacci(n - 1) 
        + recursiveFibonacci(n - 2);
    }

    public static int iterativeFibonacci(int n) {
        if (n < 2) {
            return n;
        }

        int ans = 0;
        int n1 = 0;
        int n2 = 1;

        for(n--; n > 0; n--) {
            ans = n1 + n2;
            n1 = n2;
            n2 = ans;
        }

        return ans;
    }
}