import java.util.*;
import java.io.*;
import java.net.*;

public class Caesar_Receiver {
    private ServerSocket server = null;
    private Socket socket = null;
    private DataInputStream input = null;
    private DataOutputStream output = null;

    public Caesar_Receiver(int port) {
        try {
            server = new ServerSocket(port);
            socket = server.accept();
            System.out.println("Client is connected!\n");
            input = new DataInputStream(socket.getInputStream());
            output = new DataOutputStream(socket.getOutputStream());
        } catch (UnknownHostException u) {
            System.out.println(u);
        } catch (IOException i) {
            System.out.println(i);
        }
    }

    String caesarDecrypt(String ct, int k) {
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

    public void Work() {
        try {
            int k = input.readInt();
            String ip = input.readUTF();
            String[] ips = ip.trim().split("\\s+");
            Vector<String> ct = new Vector<>();
            for (String word : ips) {
                ct.add(caesarDecrypt(word, k));
            }
            System.out.println("The received encrypted text is: " + ip);
            System.out.println("The received key is: " + k);
            String cts = String.join(" ", ct);
            System.out.println("The decrypted text is: " + cts);
            output.writeUTF("Success from receiver!");
            input.close();
            output.close();
        } catch (IOException i) {
            System.out.println(i);
        }
    }

    public static void main(String[] args) {
        Caesar_Receiver cs = new Caesar_Receiver(5431);
        cs.Work();
    }
}
