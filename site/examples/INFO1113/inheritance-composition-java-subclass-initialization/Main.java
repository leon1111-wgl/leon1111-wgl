// Leon | Original learning example
// Preserve a superclass contract
public class Main {
    static class Counter {
        private int value;
        Counter(int start) {
            if (start < 0)
                throw new IllegalArgumentException();
            value = start;
        }
        void add(int amount) {
            if (amount < 0 || amount > Integer.MAX_VALUE - value)
                throw new IllegalArgumentException();
            value += amount;
        }
        int value() {
            return value;
        }
        String describe() {
            return "count=" + value;
        }
    }
    static final class NamedCounter extends Counter {
        private final String name;
        NamedCounter(String name, int start) {
            super(start);
            this.name = name;
        }
        @Override
        String describe() {
            return name + "=" + value();
        }
    }
    public static void main(String[] args) {
        Counter counter = new NamedCounter("samples", 2);
        counter.add(3);
        System.out.println(counter.describe());
        try {
            counter.add(-1);
        } catch (IllegalArgumentException ex) {
            System.out.println("negative rejected");
        }
        System.out.println("count=" + counter.value());
    }
}
