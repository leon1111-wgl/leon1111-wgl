// Leon | Original learning example
// A hierarchy, a wrapped cause and an unchecked contract error
public class Main {
    /** Base type for every problem with an order line. Checked, so callers must plan for it. */
    static class OrderException extends Exception {
        private static final long serialVersionUID = 1L;

        OrderException(String message) {
            super(message);
        }

        OrderException(String message, Throwable cause) {
            super(message, cause);
        }
    }

    /** A more specific kind of order problem: callers may catch it on its own. */
    static final class UnknownItemException extends OrderException {
        private static final long serialVersionUID = 1L;
        private final String code;

        UnknownItemException(String code) {
            super("no such item: " + code);
            this.code = code;
        }

        String getCode() {
            return code;
        }
    }

    /** Unchecked: a caller that passes a bad number has a bug, not a situation to handle. */
    static final class InvalidQuantityException extends RuntimeException {
        private static final long serialVersionUID = 1L;

        InvalidQuantityException(int quantity) {
            super("quantity must be at least 1 but was " + quantity);
        }
    }

    /** Low-level helper: reports the first bad character with a plain unchecked exception. */
    static int readNumber(String text) {
        int value = 0;
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c < '0' || c > '9') {
                throw new IllegalArgumentException("'" + c + "' is not a digit");
            }
            value = value * 10 + (c - '0');
        }
        return value;
    }

    static int priceOf(String code) throws UnknownItemException {
        if (code.equals("tea")) {
            return 300;
        }
        if (code.equals("cake")) {
            return 450;
        }
        throw new UnknownItemException(code);
    }

    /** Translate a low-level failure into this layer's own exception and keep the cause. */
    static int total(String line) throws OrderException {
        String[] parts = line.split(":");
        int price = priceOf(parts[0]);
        int quantity;
        try {
            quantity = readNumber(parts[1]);
        } catch (IllegalArgumentException cause) {
            throw new OrderException("bad quantity in \"" + line + "\"", cause);
        }
        if (quantity < 1) {
            throw new InvalidQuantityException(quantity);
        }
        return price * quantity;
    }

    public static void main(String[] args) {
        String[] lines = {"tea:2", "juice:1", "cake:x3", "cake:0"};
        for (String line : lines) {
            try {
                System.out.println(line + " -> " + total(line) + " cents");
            } catch (UnknownItemException ex) {
                System.out.println(line + " -> unknown code " + ex.getCode());
            } catch (OrderException ex) {
                System.out.println(line + " -> " + ex.getMessage() + ", cause: " + ex.getCause().getMessage());
            } catch (InvalidQuantityException ex) {
                System.out.println(line + " -> contract violated: " + ex.getMessage());
            } finally {
                System.out.println("  processed " + line);
            }
        }
    }
}
