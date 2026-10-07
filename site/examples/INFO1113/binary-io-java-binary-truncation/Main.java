// Leon | Original learning example
// Inspect exact bytes and reject truncation
import java.io.*;

public class Main {

    public static void main(String[] args) throws Exception {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        try (DataOutputStream out = new DataOutputStream(bytes)) {
            out.writeInt(258);
        }
        byte[] full = bytes.toByteArray();
        StringBuilder hex = new StringBuilder();
        for (byte value : full) {
            if (hex.length() > 0)
                hex.append(' ');
            hex.append(String.format(java.util.Locale.ROOT, "%02X", value & 0xff));
        }
        System.out.println("hex=" + hex);
        byte[] shortRecord = java.util.Arrays.copyOf(full, 3);
        try (DataInputStream in =
                 new DataInputStream(new ByteArrayInputStream(shortRecord))) {
            in.readInt();
            System.out.println("unexpected complete record");
        } catch (EOFException ex) {
            System.out.println("truncated int rejected");
        }
    }
}
