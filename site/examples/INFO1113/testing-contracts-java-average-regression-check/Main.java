// Guoliang | Original learning example
// Keep a focused arithmetic regression test
public class Main {
    static double average(int[] values) {
        if (values.length == 0)
            throw new IllegalArgumentException("empty input");
        long sum = 0;
        for (int value : values)
            sum += value;
        return (double)sum / values.length;
    }
    public static void main(String[] args) {
        int[] values = {3, 6};
        double actual = average(values);
        if (actual != 4.5)
            throw new AssertionError("expected 4.5");
        boolean rejected = false;
        try {
            average(new int[0]);
        } catch (IllegalArgumentException ex) {
            rejected = true;
        }
        if (!rejected)
            throw new AssertionError("empty input must fail");
        System.out.println("fractional average=" + actual);
        System.out.println("empty input rejected=" + rejected);
    }
}
