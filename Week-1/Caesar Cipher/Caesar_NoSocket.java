import java.util.*;

public class Caesar_NoSocket {
    static String caesarEncrypt(String pt, int k) {
        StringBuilder ct = new StringBuilder();

        for (char c : pt.toCharArray()) {
            if (Character.isUpperCase(c)) {
                int ch = (int) c - 'A';
                ch = (ch + k) % 26;
                char cs = (char) (ch + 65);
                ct.append(cs);
            } else if (Character.isLowerCase(c)) {
                int ch = (int) c - 'a';
                ch = (ch + k) % 26;
                char cs = (char) (ch + 97);
                ct.append(cs);
            } else {
                ct.append(c);
            }
        }

        return ct.toString();
    }

    static String caesarDecrypt(String ct, int k) {
        StringBuilder pt = new StringBuilder();

        for (char c : ct.toCharArray()) {
            if (Character.isUpperCase(c)) {
                int ch = (int) c - 'A';
                ch = (ch - k) % 26;
                if (ch < 0) {
                    ch += 26;
                }
                char cs = (char) (ch + 65);
                pt.append(cs);
            } else if (Character.isLowerCase(c)) {
                int ch = (int) c - 'a';
                ch = (ch - k) % 26;
                if (ch < 0) {
                    ch += 26;
                }
                char cs = (char) (ch + 97);
                pt.append(cs);
            } else {
                pt.append(c);
            }
        }

        return pt.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter the message: ");
        String[] ips = sc.nextLine().trim().split("\\s+");
        System.out.print("Enter the key: ");
        int k = sc.nextInt();
        Vector<String> ct = new Vector<>();
        Vector<String> pt = new Vector<>();
        for (String word : ips) {
            ct.add(caesarEncrypt(word, k));
        }
        for (String word : ct) {
            pt.add(caesarDecrypt(word, k));
        }
        System.out.println("The encrypted text is: " + String.join(" ", ct));
        System.out.println("The decrypted text is: " + String.join(" ", pt));
        sc.close();
    }
}