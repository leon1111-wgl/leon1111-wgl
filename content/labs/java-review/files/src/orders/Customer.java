package orders;

public class Customer {
    private final String name;
    private final String email;     // null for a guest checkout

    public Customer(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public String getName() {
        return name;
    }

    /** The contact address, or null if the customer checked out as a guest. */
    public String getEmail() {
        return email;
    }
}
