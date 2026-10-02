// Guoliang | Original learning example
// Separate parsing from accepted range
public class Main {

    public static void main(String[] args) {
        for (String text : new String[] {"12", "-2", "twelve", "2147483648"}) {
            try {
                int value = Integer.parseInt(text);
                if (value < 0)
                    System.out.println(text + ": negative count");
                else
                    System.out.println(text + ": accepted " + value);
            } catch (NumberFormatException ex) {
                System.out.println(text + ": invalid int text");
            }
        }
    }
}
