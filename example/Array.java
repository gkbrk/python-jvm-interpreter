package jvmtest;

class ArrayTest {
    public static void insertionSort(int[] A){
        for(int i = 1; i < A.length; i++){
            int value = A[i];
            int j = i - 1;
            while(j >= 0 && A[j] > value){
                A[j + 1] = A[j];
                j = j - 1;
            }
            A[j + 1] = value;
        }
    }

    public static void cocktailSort( int[] A ){
        boolean swapped;
        do {
            swapped = false;
            for (int i =0; i<=  A.length  - 2;i++) {
                if (A[ i ] > A[ i + 1 ]) {
                    //test whether the two elements are in the wrong order
                    int temp = A[i];
                    A[i] = A[i+1];
                    A[i+1]=temp;
                    swapped = true;
                }
            }
            if (!swapped) {
                //we can exit the outer loop here if no swaps occurred.
                break;
            }
            swapped = false;
            for (int i= A.length - 2;i>=0;i--) {
                if (A[ i ] > A[ i + 1 ]) {
                    int temp = A[i];
                    A[i] = A[i+1];
                    A[i+1]=temp;
                    swapped = true;
                }
            }
            //if no elements have been swapped, then the list is sorted
	} while (swapped);
    }

    public static int sum(int[] array) {
        int total = 0;
        for (int element : array) {
            total += element;
        }
        return total;
    }

    public static String loopMultipleArray() {
        StringBuilder result = new StringBuilder();
        
        String[] a = {"a","b","c"};
        String[] b = {"A","B","C"};
        int[] c = {1,2,3};

        for(int i = 0;i < a.length;i++){
            result.append(a[i] + b[i] + c[i] + '\n');
        }

        return result.toString();
    }
}
