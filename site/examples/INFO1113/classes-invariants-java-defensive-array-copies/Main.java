// Leon | Original learning example
// Protect an internal array
import java.util.Arrays;

public class Main {
    static final class Snapshot {
        private final int[] values;
        Snapshot(int[] values) {
            this.values = values.clone();
        }
        int[] values() {
            return values.clone();
        }
    }
    public static void main(String[] args) {
        int[] supplied = {2, 5};
        Snapshot snapshot = new Snapshot(supplied);
        supplied[0] = 99;
        int[] exported = snapshot.values();
        exported[1] = 77;
        System.out.println("supplied=" + Arrays.toString(supplied));
        System.out.println("exported=" + Arrays.toString(exported));
        System.out.println("protected=" + Arrays.toString(snapshot.values()));
    }
}
