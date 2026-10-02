// Guoliang | Original learning example
// Trace overload then override
public class Main {
    static class Printer {
        String show(Object value) {
            return "general";
        }
        String show(String value) {
            return "text";
        }
    }
    static final class FancyPrinter extends Printer {
        @Override
        String show(Object value) {
            return "fancy general";
        }
    }
    public static void main(String[] args) {
        Printer p = new FancyPrinter();
        Object item = "hello";
        System.out.println(p.show(item));
        System.out.println(p.show("hello"));
    }
}
