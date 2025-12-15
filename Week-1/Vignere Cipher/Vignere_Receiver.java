import java.util.*;
import java.io.*;
import java.net.*;

public class Vignere_Receiver {
    private ServerSocket server = null;
    private Socket socket = null;
    private DataInputStream input = null;
    private DataOutputStream output = null;
    int pos = 0;

    public Vignere_Receiver(int port) {
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

    String vignereDecrypt(String ct, String k) {
        StringBuilder pt = new StringBuilder();
        int klen = k.length();

        for (char c : ct.toCharArray()) {
            char keyChar = k.charAt(pos);
            int shift;
            if (Character.isUpperCase(keyChar)) {
                shift = keyChar - 'A';
            } else {
                shift = keyChar - 'a';
            }

            if (Character.isUpperCase(c)) {
                int ch = (int) c - 'A';
                ch = (ch - shift) % 26;
                if (ch < 0) {
                    ch += 26;
                }
                char vr = (char) (ch + 65);
                pt.append(vr);
                pos = (pos + 1) % klen;
            } else if (Character.isLowerCase(c)) {
                int ch = (int) c - 'a';
                ch = (ch - shift) % 26;
                if (ch < 0) {
                    ch += 26;
                }
                char vr = (char) (ch + 97);
                pt.append(vr);
                pos = (pos + 1) % klen;
            } else {
                pt.append(c);
            }
        }

        return pt.toString();
    }

    public void Work() {
        try {
            String k = input.readUTF();
            String ip = input.readUTF();
            String[] ips = ip.trim().split("\\s+");
            Vector<String> ct = new Vector<>();
            for (String word : ips) {
                ct.add(vignereDecrypt(word, k));
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
        Vignere_Receiver vr = new Vignere_Receiver(5431);
        vr.Work();
    }
}
