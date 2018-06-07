package jvmtest;

class InstanceTest {
    public int num;

    public InstanceTest() {
        num = 0;
    }

    public void set_num(int n) {
        num = n;
    }

    public int get_num() {
        return num;
    }

    public static int test_single() {
        InstanceTest i = new InstanceTest();

        i.set_num(12345);

        return i.get_num();
    }
}