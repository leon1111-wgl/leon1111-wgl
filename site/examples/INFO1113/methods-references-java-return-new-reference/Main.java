// Guoliang | Original learning example
// Return a replacement deliberately
import java.util.Arrays;

public class Main {
    static void increment(Integer x) {
        x++;
        System.out.println("local count=" + x);
    }
    static int[] doubled(int[] input) {
        int[] result = input.clone();
        for (int i = 0; i < result.length; i++)
            result[i] *= 2;
        return result;
    }
    public static void main(String[] args) {
        Integer count = 4;
        increment(count);
        System.out.println("caller count=" + count);
        int[] values = {2, 5};
        int[] replacement = doubled(values);
        System.out.println("original=" + Arrays.toString(values));
        values = replacement;
        System.out.println("adopted=" + Arrays.toString(values));
    }
}
