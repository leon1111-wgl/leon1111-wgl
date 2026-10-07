// Leon | Original learning example
// Validate complete equipment records
import java.io.BufferedReader;
import java.io.StringReader;

public class Main {

    public static void main(String[] args) throws Exception {
        String data = "lamp,3\nchair,5\ndesk,many\nshelf,-2\n";
        int total = 0, lineNumber = 0;
        try (BufferedReader reader = new BufferedReader(new StringReader(data))) {
            String line;
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                String[] fields = line.split(",", -1);
                if (fields.length != 2 || fields[0].trim().isEmpty()) {
                    System.out.println("line " + lineNumber + ": bad structure");
                    continue;
                }
                try {
                    int count = Integer.parseInt(fields[1].trim());
                    if (count < 0) {
                        System.out.println("line " + lineNumber + ": negative count");
                        continue;
                    }
                    total += count;
                } catch (NumberFormatException ex) {
                    System.out.println("line " + lineNumber + ": bad integer");
                }
            }
        }
        System.out.println("accepted total=" + total);
    }
}
