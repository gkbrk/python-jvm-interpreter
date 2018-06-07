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

    public static int test_multiple_1() {
        InstanceTest i1 = new InstanceTest();
        InstanceTest i2 = new InstanceTest();

        i1.set_num(12345);
        i2.set_num(54321);

        return i1.get_num();
    }

    public static int test_multiple_2() {
        InstanceTest i1 = new InstanceTest();
        InstanceTest i2 = new InstanceTest();

        i1.set_num(12345);
        i2.set_num(54321);

        return i2.get_num();
    }
}