// Leon | Original learning example
// Trace the processed prefix
public class Main {

    public static void main(String[] args) {
        int[] values = {4, 0, 7};
        int total = 0;
        for (int i = 0; i < values.length; i++) {
            total += values[i];
            System.out.println("processed=" + (i + 1) + ", total=" + total);
        }
        int emptyTotal = 0;
        for (int value : new int[0])
            emptyTotal += value;
        System.out.println("empty total=" + emptyTotal);
    }
}
