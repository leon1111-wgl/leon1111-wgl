// Leon | Original learning example
// Write and read a sensor record
import java.io.*;

public class Main {

    public static void main(String[] args) throws Exception {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        try (DataOutputStream out = new DataOutputStream(bytes)) {
            out.writeInt(258);
            out.writeDouble(18.5);
        }
        byte[] record = bytes.toByteArray();
        System.out.println("bytes=" + record.length);
        try (DataInputStream in =
                 new DataInputStream(new ByteArrayInputStream(record))) {
            System.out.println("station=" + in.readInt());
            System.out.println("temperature=" + in.readDouble());
            System.out.println("at end=" + (in.read() == -1));
        }
    }
}
