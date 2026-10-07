// Leon | Original learning example
// Protect a capacity invariant
public class Main {
    static final class Dispenser {
        private final int capacity;
        private int level;
        Dispenser(int capacity, int level) {
            if (capacity < 0 || level < 0 || level > capacity)
                throw new IllegalArgumentException("invalid state");
            this.capacity = capacity;
            this.level = level;
        }
        void fill(int amount) {
            if (amount < 0 || amount > capacity - level)
                throw new IllegalArgumentException("does not fit");
            level += amount;
        }
        int level() {
            return level;
        }
    }
    public static void main(String[] args) {
        Dispenser a = new Dispenser(12, 4);
        Dispenser b = new Dispenser(8, 0);
        a.fill(5);
        System.out.println("after fill=" + a.level());
        try {
            a.fill(4);
        } catch (IllegalArgumentException ex) {
            System.out.println("rejected");
        }
        System.out.println("after rejection=" + a.level());
        System.out.println("other instance=" + b.level());
    }
}
