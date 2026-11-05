package shop;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Tracks how many units of each SKU a warehouse holds. */
public class Inventory {
    private final Map<String, Integer> stock = new HashMap<String, Integer>();

    /** Adds qty units of sku. The sku must not be blank and qty must be positive. */
    public void add(String sku, int qty) {
        if (sku == null || sku.trim().isEmpty()) {
            throw new IllegalArgumentException("sku must not be blank");
        }
        if (qty <= 0) {
            throw new IllegalArgumentException("quantity must be positive: " + qty);
        }
        int current = stockOf(sku);
        if (current > Integer.MAX_VALUE - qty) {
            throw new ArithmeticException("stock overflow for " + sku);
        }
        stock.put(sku, current + qty);
    }

    /**
     * Removes qty units of sku. Fails with InsufficientStockException if the sku
     * is unknown or holds fewer than qty units; a failed remove changes nothing.
     */
    public void remove(String sku, int qty) {
        if (qty <= 0) {
            throw new IllegalArgumentException("quantity must be positive: " + qty);
        }
        int current = stockOf(sku);
        if (qty >= current) {
            throw new InsufficientStockException(sku, qty, current);
        }
        stock.put(sku, current - qty);
    }

    /** Units held for sku; 0 for a sku that was never added. */
    public int stockOf(String sku) {
        Integer units = stock.get(sku);
        return units == null ? 0 : units;
    }

    /** SKUs holding strictly fewer than threshold units, in alphabetical order. */
    public List<String> lowStock(int threshold) {
        List<String> result = new ArrayList<String>();
        for (Map.Entry<String, Integer> entry : stock.entrySet()) {
            if (entry.getValue() < threshold) {
                result.add(entry.getKey());
            }
        }
        Collections.sort(result);
        return result;
    }
}
