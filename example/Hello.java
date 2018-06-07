package com.gkbrk.JVMTest;

import com.gkbrk.JVMTest.TestImport;
import jstdlib.Rng;

class Hello {
    public static final String greeting = "Hi";

    public static void main(String[] args) {
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
        //fizzbuzz();
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

    public static void fizzbuzz() {
        for(int i= 1; i <= 100; i++){
            if(i % 15 == 0){
                System.out.println("FizzBuzz");
            }else if(i % 3 == 0){
                System.out.println("Fizz");
            }else if(i % 5 == 0){
                System.out.println("Buzz");
            }else{
                System.out.println(i);
            }
        }
    }

    public static double monteCarloPi(int n){
        int inCircle = 0;

        for (int i = 0; i < n; i++) {
            // a square with a side of length 2 centered at 0 has 
            // x and y range of -1 to 1
            double randX = Math.random() * 2 - 1; //range -1 to 1
            double randY = Math.random() * 2 - 1; //range -1 to 1
            double dist = Math.sqrt(randX * randX + randY * randY);

            if(dist < 1) {
                inCircle++;
            }
        }

        return 4.0 * inCircle / n;
    }
}