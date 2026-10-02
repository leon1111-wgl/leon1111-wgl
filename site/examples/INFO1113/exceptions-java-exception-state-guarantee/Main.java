// Guoliang | Original learning example
// Reject before mutating state
public class Main {
    static final class Store {
        private final int capacity;
        private int size;
        Store(int capacity, int size) {
            if (capacity < 0 || size < 0 || size > capacity)
                throw new IllegalArgumentException("invalid state");
            this.capacity = capacity;
            this.size = size;
        }
        void add(int amount) {
            if (amount < 0 || amount > capacity - size)
                throw new IllegalArgumentException("capacity exceeded");
            size += amount;
        }
        int size() {
            return size;
        }
    }
    public static void main(String[] args) {
        Store store = new Store(6, 5);
        try {
            store.add(2);
        } catch (IllegalArgumentException ex) {
            System.out.println("rejected: " + ex.getMessage());
        }
        System.out.println("after failure=" + store.size());
        store.add(1);
        System.out.println("after success=" + store.size());
    }
}
