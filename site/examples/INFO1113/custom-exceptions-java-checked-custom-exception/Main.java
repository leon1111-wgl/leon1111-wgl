// Leon | Original learning example
// A checked exception that carries data
public class Main {
    /** Checked: the caller can often fix this, so the compiler makes callers face it. */
    static final class InsufficientFundsException extends Exception {
        private static final long serialVersionUID = 1L;
        private final int shortfall;

        InsufficientFundsException(String message, int shortfall) {
            super(message);
            this.shortfall = shortfall;
        }

        int getShortfall() {
            return shortfall;
        }
    }

    static final class Wallet {
        private int cents;

        Wallet(int cents) {
            this.cents = cents;
        }

        int balance() {
            return cents;
        }

        void topUp(int amount) {
            cents += amount;
        }

        void pay(int price) throws InsufficientFundsException {
            if (price <= 0) {
                throw new IllegalArgumentException("price must be positive: " + price);
            }
            if (price > cents) {
                int missing = price - cents;
                throw new InsufficientFundsException("need " + missing + " more cents", missing);
            }
            cents -= price;
        }
    }

    public static void main(String[] args) {
        Wallet wallet = new Wallet(250);
        try {
            wallet.pay(200);
            System.out.println("paid 200, balance " + wallet.balance());
            wallet.pay(100);
            System.out.println("this line is skipped");
        } catch (InsufficientFundsException ex) {
            System.out.println("caught: " + ex.getMessage());
            System.out.println("balance unchanged: " + wallet.balance());
            wallet.topUp(ex.getShortfall());
            System.out.println("topped up " + ex.getShortfall() + ", balance " + wallet.balance());
            try {
                wallet.pay(100);
                System.out.println("second try paid 100, balance " + wallet.balance());
            } catch (InsufficientFundsException again) {
                System.out.println("still short: " + again.getShortfall());
            }
        }

        try {
            wallet.pay(-5);
        } catch (InsufficientFundsException ex) {
            System.out.println("not reached: a negative price is not a funds problem");
        } catch (IllegalArgumentException ex) {
            System.out.println("programming error: " + ex.getMessage());
        }
    }
}
