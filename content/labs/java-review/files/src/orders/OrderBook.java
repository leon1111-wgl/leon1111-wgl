package orders;

import java.util.ArrayList;
import java.util.List;

/** The orders waiting for payment. */
public class OrderBook {
    private final List<Order> orders = new ArrayList<Order>();

    public void add(Order order) {
        orders.add(order);
    }

    public int size() {
        return orders.size();
    }

    /** The ids of the orders still in the book, in the order they were added. */
    public List<String> ids() {
        List<String> ids = new ArrayList<String>();
        for (Order order : orders) {
            ids.add(order.getId());
        }
        return ids;
    }

    /** Removes every order that expired at or before now. Returns how many were removed. */
    public int purgeExpired(long now) {
        int removed = 0;
        for (Order order : orders) {
            if (order.isExpired(now)) {
                orders.remove(order);
                removed++;
            }
        }
        return removed;
    }

    /** One line per order for the daily summary email. */
    public List<String> summaryLines() {
        List<String> lines = new ArrayList<String>();
        for (Order order : orders) {
            String email = order.getCustomer().getEmail().toLowerCase();
            lines.add(order.getId() + " " + order.getCustomer().getName() + " <" + email + "> x" + order.getUnits());
        }
        return lines;
    }
}
