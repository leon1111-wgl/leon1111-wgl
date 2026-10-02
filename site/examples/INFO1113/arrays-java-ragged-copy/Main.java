// Guoliang | Original learning example
// Trace shallow and row-wise copies
import java.util.Arrays;

public class Main {

    public static void main(String[] args) {
        int[][] original = {{2, 5}, {9}};
        int[][] shallow = original.clone();
        shallow[0][1] = 7;
        shallow[1] = new int[] {4, 6, 8};
        System.out.println("original=" + Arrays.deepToString(original));
        System.out.println("shallow=" + Arrays.deepToString(shallow));
        int[][] isolated = new int[original.length][];
        for (int i = 0; i < original.length; i++)
            isolated[i] = original[i].clone();
        isolated[0][0] = 99;
        System.out.println("original after isolated edit=" +
                           Arrays.deepToString(original));
    }
}
