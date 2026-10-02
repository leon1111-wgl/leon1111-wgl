// Guoliang | Original learning example
// Turn documentation into executable checks
public class Main {
    /**
     * Returns the nonnegative distance between two nonnegative positions.
     * @throws IllegalArgumentException if either position is negative
     */
    static long distance(int left, int right) {
        if (left < 0 || right < 0)
            throw new IllegalArgumentException("negative position");
        return Math.abs((long)left - right);
    }
    public static void main(String[] args) {
        System.out.println("distance=" + distance(2, 9));
        try {
            distance(-1, 9);
        } catch (IllegalArgumentException ex) {
            System.out.println("rejected negative position");
        }
    }
}
