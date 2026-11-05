package orders;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Arrays;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class OrderBookTest {
    private static final long NOW = 10000L;
    private OrderBook book;

    private static Order order(String id, String email, long expiresAt) {
        return new Order(id, new Customer("Test " + id, email), 1, expiresAt);
    }

    @BeforeEach
    void setUp() {
        book = new OrderBook();
        book.add(order("A-100", "leon@example.test", 5000L));       // expired
        book.add(order("A-101", "mia@example.test", 20000L));
        book.add(order("A-102", "emma@example.test", 8000L));       // expired
        book.add(order("A-103", null, 30000L));                     // guest, no email
        book.add(order("A-104", "jack@example.test", 40000L));
    }

    @Test
    void purgeRemovesEveryExpiredOrder() {
        assertEquals(2, book.purgeExpired(NOW));
        assertEquals(3, book.size());
    }

    @Test
    void purgeKeepsOrdersThatHaveNotExpired() {
        book.purgeExpired(NOW);
        assertEquals(Arrays.asList("A-101", "A-103", "A-104"), book.ids());
    }

    @Test
    void adjacentExpiredOrdersAreAllRemoved() {
        OrderBook small = new OrderBook();
        small.add(order("B-1", "a@example.test", 20000L));
        small.add(order("B-2", "b@example.test", 1000L));           // expired
        small.add(order("B-3", "c@example.test", 2000L));           // expired, right after B-2
        assertEquals(2, small.purgeExpired(NOW));
        assertEquals(Arrays.asList("B-1"), small.ids());
    }

    @Test
    void purgeOnEmptyBookRemovesNothing() {
        assertEquals(0, new OrderBook().purgeExpired(NOW));
    }

    @Test
    void summaryLowercasesEmail() {
        OrderBook one = new OrderBook();
        one.add(order("C-1", "Mia@Example.TEST", 20000L));
        assertEquals(Arrays.asList("C-1 Test C-1 <mia@example.test> x1"), one.summaryLines());
    }

    @Test
    void summaryShowsGuestWithoutEmail() {
        book.purgeExpired(NOW);
        assertEquals("A-103 Test A-103 <no email on file> x1", book.summaryLines().get(1));
    }
}
