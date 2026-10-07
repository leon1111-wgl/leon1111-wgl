// Leon | Original learning example
// Compare mutation with reassignment
import java.util.Arrays;

public class Main {
    static void change(int[] x) {
        x[0] = 10;
        System.out.println("after mutation=" + Arrays.toString(x));
        x = new int[] {1, 2};
        System.out.println("local replacement=" + Arrays.toString(x));
    }
    public static void main(String[] args) {
        int[] scores = {6, 8};
        change(scores);
        System.out.println("caller=" + Arrays.toString(scores));
    }
}
