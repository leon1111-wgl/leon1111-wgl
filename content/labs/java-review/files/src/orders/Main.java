package orders;

/** Builds a small order book, drops expired orders and prints the daily summary. */
public class Main {
    public static void main(String[] args) {
        long now = 10000L;
        OrderBook book = new OrderBook();
        book.add(new Order("A-100", new Customer("Leon", "Leon@Example.test"), 3, 5000L));    // expired
        book.add(new Order("A-101", new Customer("Mia", "mia@example.test"), 1, 20000L));
        book.add(new Order("A-102", new Customer("Emma", "emma@example.test"), 2, 8000L));    // expired
        book.add(new Order("A-103", new Customer("Guest", null), 5, 30000L));                 // guest checkout
        book.add(new Order("A-104", new Customer("Jack", "jack@example.test"), 4, 40000L));

        int removed = book.purgeExpired(now);
        System.out.println("purged " + removed + " expired orders, " + book.size() + " left");
        for (String line : book.summaryLines()) {
            System.out.println(line);
        }
    }
}
