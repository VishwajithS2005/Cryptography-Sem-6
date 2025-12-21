import java.util.*;
import java.io.*;
import java.net.*;

public class Vernam_Sender {
    private Socket socket = null;
    private DataInputStream input = null;
    private DataOutputStream output = null;
    private Scanner sc = null;
    int pos = 0;

    public Vernam_Sender(String address, int port) {
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

    String vernamEncrypt(String pt, String k) {
        StringBuilder ct = new StringBuilder();
        for (int i = 0; i < pt.length(); i++) {
            char pChar = pt.charAt(i);
            char kChar = k.charAt(i);
            int pc, kc;
            if (Character.isUpperCase(pChar)) {
                pc = (int) pChar - 'A';
            } else {
                pc = (int) pChar - 'a';
            }
            if (Character.isUpperCase(kChar)) {
                kc = (int) kChar - 'A';
            } else {
                kc = (int) kChar - 'a';
            }
            int cc = (pc ^ kc);
            if (Character.isUpperCase(pChar)) {
                char cChar = (char) (cc + 'A');
                ct.append(cChar);
            } else {
                char cChar = (char) (cc + 'a');
                ct.append(cChar);
            }
        }
        return ct.toString();
    }

    public void Work() {
        try {
            System.out.print("Enter the message: ");
            String ips = sc.next().trim();
            System.out.print("Enter the key: ");
            String k = sc.next().trim();
            String cts = vernamEncrypt(ips, k);
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
        Vernam_Sender vs = new Vernam_Sender("127.0.0.1", 5431);
        vs.Work();
    }
}
