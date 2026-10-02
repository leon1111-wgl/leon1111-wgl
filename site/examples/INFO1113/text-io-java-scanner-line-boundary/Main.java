// Guoliang | Original learning example
// Observe a token followed by a line
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner("12\nlamp\n")) {
            int count = scanner.nextInt();
            String remainder = scanner.nextLine();
            String name = scanner.nextLine();
            System.out.println("count=" + count);
            System.out.println("remainder length=" + remainder.length());
            System.out.println("name=" + name);
        }
    }
}
