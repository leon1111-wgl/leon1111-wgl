package orders;

public class Order {
    private final String id;
    private final Customer customer;
    private final int units;
    private final long expiresAt;   // epoch milliseconds

    public Order(String id, Customer customer, int units, long expiresAt) {
        this.id = id;
        this.customer = customer;
        this.units = units;
        this.expiresAt = expiresAt;
    }

    public String getId() {
        return id;
    }

    public Customer getCustomer() {
        return customer;
    }

    public int getUnits() {
        return units;
    }

    /** An unpaid order expires at its deadline: true when now is at or past it. */
    public boolean isExpired(long now) {
        return now >= expiresAt;
    }
}
