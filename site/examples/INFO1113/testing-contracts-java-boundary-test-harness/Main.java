// Guoliang | Original learning example
// Run boundary tests without a test dependency
public class Main {
    static final class Seats {
        private int reserved = 3;
        void reserve(int amount) {
            if (amount < 0 || amount > 8 - reserved)
                throw new IllegalArgumentException();
            reserved += amount;
        }
    }
    static void check(boolean condition) {
        if (!condition)
            throw new AssertionError("contract failed");
    }
    static void testSuccess(int amount, int expected) {
        Seats seats = new Seats();
        seats.reserve(amount);
        check(seats.reserved == expected);
    }
    static void testReject(int amount) {
        Seats seats = new Seats();
        boolean rejected = false;
        try {
            seats.reserve(amount);
        } catch (IllegalArgumentException ex) {
            rejected = true;
        }
        check(rejected);
        check(seats.reserved == 3);
    }
    public static void main(String[] args) {
        testSuccess(2, 5);
        testSuccess(5, 8);
        testReject(6);
        testReject(-1);
        System.out.println("four contract cases passed");
    }
}
