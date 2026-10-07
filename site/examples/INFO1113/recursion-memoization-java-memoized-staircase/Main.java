// Leon | Original learning example
// Cache each staircase state once
import java.util.*;

public class Main {
    static long ways(int n, Map<Integer, Long> memo, int[] computed) {
        if (n < 0 || n > 91)
            throw new IllegalArgumentException("supported range 0..91");
        Long cached = memo.get(n);
        if (cached != null)
            return cached;
        computed[0]++;
        long result = n < 2 ? 1L
                            : Math.addExact(ways(n - 1, memo, computed),
                                            ways(n - 2, memo, computed));
        memo.put(n, result);
        return result;
    }
    public static void main(String[] args) {
        Map<Integer, Long> memo = new HashMap<>();
        int[] computed = {0};
        System.out.println("ways(4)=" + ways(4, memo, computed));
        System.out.println("computed states=" + computed[0]);
        System.out.println("repeat=" + ways(4, memo, computed));
        System.out.println("computed after repeat=" + computed[0]);
    }
}
