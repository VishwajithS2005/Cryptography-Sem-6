import java.util.*;
import java.io.*;
import java.net.*;

public class Caesar_Sender {
    private Socket socket = null;
    private DataInputStream input = null;
    private DataOutputStream output = null;
    private Scanner sc = null;

    public Caesar_Sender(String address, int port) {
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

    String caesarEncrypt(String pt, int k) {
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

    public void Work() {
        try {
            System.out.print("Enter the message: ");
            String[] ips = sc.nextLine().trim().split("\\s+");
            System.out.print("Enter the key: ");
            int k = sc.nextInt();
            Vector<String> ct = new Vector<>();
            for (String word : ips) {
                ct.add(caesarEncrypt(word, k));
            }
            String cts = String.join(" ", ct);
            System.out.println("The encrypted text is: " + cts);
            output.writeInt(k);
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
        Caesar_Sender cc = new Caesar_Sender("127.0.0.1", 5431);
        cc.Work();
    }
}
