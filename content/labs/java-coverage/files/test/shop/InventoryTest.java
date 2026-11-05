package shop;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.Arrays;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class InventoryTest {
    private Inventory inv;

    @BeforeEach
    void setUp() {
        inv = new Inventory();          // a fresh warehouse for every test
    }

    @Test
    void addThenStockOf() {
        inv.add("DESK-OAK", 4);
        assertEquals(4, inv.stockOf("DESK-OAK"));
    }

    @Test
    void addAccumulates() {
        inv.add("LAMP-01", 2);
        inv.add("LAMP-01", 3);
        assertEquals(5, inv.stockOf("LAMP-01"));
    }

    @Test
    void removeReducesStock() {
        inv.add("DESK-OAK", 10);
        inv.remove("DESK-OAK", 4);
        assertEquals(6, inv.stockOf("DESK-OAK"));
    }

    @Test
    void removeMoreThanStockThrows() {
        inv.add("DESK-OAK", 4);
        InsufficientStockException ex = assertThrows(InsufficientStockException.class,
                () -> inv.remove("DESK-OAK", 5));
        assertEquals("DESK-OAK", ex.getSku());
        assertEquals(5, ex.getRequested());
        assertEquals(4, ex.getAvailable());
        assertEquals(4, inv.stockOf("DESK-OAK"));       // a failed remove changes nothing
    }

    @Test
    void removeUnknownSkuThrows() {
        InsufficientStockException ex = assertThrows(InsufficientStockException.class,
                () -> inv.remove("GHOST-99", 1));
        assertEquals(0, ex.getAvailable());
    }

    @Test
    void lowStockIsSortedAndStrict() {
        inv.add("LAMP-01", 3);
        inv.add("DESK-OAK", 9);
        inv.add("CHAIR-02", 10);                        // exactly at the threshold: not low
        assertEquals(Arrays.asList("DESK-OAK", "LAMP-01"), inv.lowStock(10));
    }

    @Test
    void removeExactStockLeavesZero() {
        inv.add("DESK-OAK", 10);
        inv.remove("DESK-OAK", 10);
        assertEquals(0, inv.stockOf("DESK-OAK"));
    }

    @Test
    void addZeroQuantityIsRejected() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> inv.add("DESK-OAK", 0));
        assertEquals("quantity must be positive: 0", ex.getMessage());
    }

    @Test
    void removeNegativeQuantityIsRejected() {
        inv.add("DESK-OAK", 3);
        assertThrows(IllegalArgumentException.class, () -> inv.remove("DESK-OAK", -1));
        assertEquals(3, inv.stockOf("DESK-OAK"));
    }

    // TODO: cover the guards in add() that the coverage report lists.
}
