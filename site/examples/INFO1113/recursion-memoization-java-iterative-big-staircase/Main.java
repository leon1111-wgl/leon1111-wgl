// Guoliang | Original learning example
// Replace deep recursion with an iterative exact count
public class Main {
    static java.math.BigInteger ways(int n) {
        if (n < 0 || n > 1000)
            throw new IllegalArgumentException("demo range 0..1000");
        java.math.BigInteger previous = java.math.BigInteger.ONE;
        java.math.BigInteger current = java.math.BigInteger.ONE;
        for (int i = 2; i <= n; i++) {
            java.math.BigInteger next = previous.add(current);
            previous = current;
            current = next;
        }
        return current;
    }
    public static void main(String[] args) {
        System.out.println("ways(0)=" + ways(0));
        System.out.println("ways(4)=" + ways(4));
        System.out.println("ways(100)=" + ways(100));
    }
}
