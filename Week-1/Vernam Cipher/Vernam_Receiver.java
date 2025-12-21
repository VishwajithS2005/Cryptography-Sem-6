import java.io.*;
import java.net.*;

public class Vernam_Receiver {
    private ServerSocket server = null;
    private Socket socket = null;
    private DataInputStream input = null;
    private DataOutputStream output = null;
    int pos = 0;

    public Vernam_Receiver(int port) {
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

    String vernamDecrypt(String ct, String k) {
        StringBuilder pt = new StringBuilder();
        for (int i = 0; i < ct.length(); i++) {
            char cChar = ct.charAt(i);
            char kChar = k.charAt(i);
            int cc, kc;
            if (Character.isUpperCase(cChar)) {
                cc = (int) cChar - 'A';
            } else {
                cc = (int) cChar - 'a';
            }
            if (Character.isUpperCase(kChar)) {
                kc = (int) kChar - 'A';
            } else {
                kc = (int) kChar - 'a';
            }
            int pc = (cc ^ kc);
            if (Character.isUpperCase(cChar)) {
                char pChar = (char) (pc + 'A');
                pt.append(pChar);
            } else {
                char pChar = (char) (pc + 'a');
                pt.append(pChar);
            }
        }
        return pt.toString();
    }

    public void Work() {
        try {
            String k = input.readUTF();
            String ip = input.readUTF();
            String cts = vernamDecrypt(ip, k);
            System.out.println("The received encrypted text is: " + ip);
            System.out.println("The received key is: " + k);
            System.out.println("The decrypted text is: " + cts);
            output.writeUTF("Success from receiver!");
            input.close();
            output.close();
        } catch (IOException i) {
            System.out.println(i);
        }
    }

    public static void main(String[] args) {
        Vernam_Receiver vr = new Vernam_Receiver(5431);
        vr.Work();
    }
}
