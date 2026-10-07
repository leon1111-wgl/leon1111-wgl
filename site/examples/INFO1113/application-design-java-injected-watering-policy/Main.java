// Leon | Original learning example
// Replace one policy without rewriting the controller
public class Main {
    static int apply(int current, java.util.function.IntUnaryOperator policy) {
        if (current < 0 || current > 10)
            throw new IllegalArgumentException("initial range");
        int amount = policy.applyAsInt(current);
        if (amount < 0 || amount > 10 - current)
            throw new IllegalArgumentException("amount range");
        return current + amount;
    }
    public static void main(String[] args) {
        java.util.function.IntUnaryOperator gentle =
            current -> Math.max(0, 6 - current);
        java.util.function.IntUnaryOperator dryDay =
            current -> Math.max(0, 8 - current);
        System.out.println("gentle=" + apply(4, gentle));
        System.out.println("dry day=" + apply(4, dryDay));
        try {
            apply(4, current -> 20);
        } catch (IllegalArgumentException ex) {
            System.out.println("unsafe policy rejected");
        }
    }
}
