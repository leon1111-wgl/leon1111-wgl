// Leon | Original learning example
// Preserve types through a box and a method
public class Main {
    static final class Box<T> {
        private final T value;
        Box(T value) {
            this.value = value;
        }
        T get() {
            return value;
        }
    }
    static <T> T first(java.util.List<T> values) {
        if (values.isEmpty())
            throw new IllegalArgumentException("empty list");
        return values.get(0);
    }
    public static void main(String[] args) {
        Box<String> direction = new Box<>("north");
        Box<Integer> count = new Box<>(8);
        String firstColor = first(java.util.Arrays.asList("red", "blue"));
        Integer firstNumber = first(java.util.Arrays.asList(8, 13));
        System.out.println(direction.get() + ", " + count.get());
        System.out.println(firstColor + ", " + firstNumber);
        try {
            first(java.util.Collections.<String>emptyList());
        } catch (IllegalArgumentException ex) {
            System.out.println("empty rejected");
        }
    }
}
