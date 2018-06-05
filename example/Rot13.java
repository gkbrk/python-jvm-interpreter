package jvmtest;

class Rot13 {
    public static void main(String[] args) {
        System.out.println(rot13("Gb trg gb gur bgure fvqr!"));
    }

    public static String rot13(String str) {
        String result = "";
        for (int i = 0; i < str.length(); i++) {
            char rot = rot13(str.charAt(i));
            result += rot;
        }
        return result;
    }

    private static char rot13(char ch) {
        if (ch >= 'A' && ch <= 'Z') {
            return (char) (((ch - 'A') + 13) % 26 + 'A');
        }
        if (ch >= 'a' && ch <= 'z') {
            return (char) (((ch - 'a') + 13) % 26 + 'a');
        }
        return ch;
    }
}