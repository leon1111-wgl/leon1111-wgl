// Guoliang | Original learning example
// Use a Number bound for a stated conversion
public class Main {
    static <T extends Number> double sum(java.util.List<T> values) {
        double total = 0.0;
        for (T value : values)
            total += value.doubleValue();
        return total;
    }
    public static void main(String[] args) {
        System.out.println("integers=" + sum(java.util.Arrays.asList(3, 7)));
        System.out.println("decimals=" + sum(java.util.Arrays.asList(2.5, 1.25)));
        System.out.println("empty=" + sum(java.util.Collections.<Integer>emptyList()));
    }
}
