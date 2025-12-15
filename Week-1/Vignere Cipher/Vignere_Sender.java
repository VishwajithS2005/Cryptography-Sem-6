import java.util.*;
import java.io.*;
import java.net.*;

public class Vignere_Sender {
    private Socket socket = null;
    private DataInputStream input = null;
    private DataOutputStream output = null;
    private Scanner sc = null;
    int pos = 0;

    public Vignere_Sender(String address, int port) {
        try {
            socket = new Socket(address, port);
            System.out.println("Client is connected!");
            input = new DataInputStream(socket.getInputStream());
            output = new DataOutputStream(socket.getOutputStream());
            sc = new Scanner(System.in);
        } catch (UnknownHostException u) {
            System.out.println(u);
        } catch (IOException i) {
            System.out.println(i);
        }
    }

    String vignereEncrpyt(String pt, String k) {
        StringBuilder ct = new StringBuilder();
        int klen = k.length();

        for (char c : pt.toCharArray()) {
            char keyChar = k.charAt(pos);
            int shift;
            if (Character.isUpperCase(keyChar)) {
                shift = keyChar - 'A';
            } else {
                shift = keyChar - 'a';
            }

            if (Character.isUpperCase(c)) {
                int ch = (int) c - 'A';
                ch = (ch + shift) % 26;
                char cs = (char) (ch + 65);
                ct.append(cs);
                pos = (pos + 1) % klen;
            } else if (Character.isLowerCase(c)) {
                int ch = (int) c - 'a';
                ch = (ch + shift) % 26;
                char cs = (char) (ch + 97);
                ct.append(cs);
                pos = (pos + 1) % klen;
            } else {
                ct.append(c);
            }
        }

        return ct.toString();
    }

    public void Work() {
        try {
            System.out.print("Enter the message: ");
            String[] ips = sc.nextLine().trim().split("\\s+");
            System.out.print("Enter the key: ");
            String k = sc.next().trim();
            Vector<String> ct = new Vector<>();
            for (String word : ips) {
                ct.add(vignereEncrpyt(word, k));
            }
            String cts = String.join(" ", ct);
            System.out.println("The encrypted text is: " + cts);
            output.writeUTF(k);
            output.writeUTF(cts);
            System.out.println(input.readUTF());
            input.close();
            output.close();
            sc.close();
        } catch (IOException i) {
            System.out.println(i);
        }
    }

    public static void main(String[] args) {
        Vignere_Sender vs = new Vignere_Sender("127.0.0.1", 5431);
        vs.Work();
    }
}
