// Guoliang | Original learning example
// Remove safely and keep reachability visible
import java.util.*;

public class Main {

    public static void main(String[] args) {
        List<Integer> values = new ArrayList<>(Arrays.asList(1, 2, 3, 4));
        List<Integer> alias = values;
        Iterator<Integer> iterator = values.iterator();
        while (iterator.hasNext()) {
            if (iterator.next() % 2 != 0)
                iterator.remove();
        }
        values = null;
        System.out.println("remaining through alias=" + alias);
        System.out.println("original variable null=" + (values == null));
        System.out.println("alias size=" + alias.size());
    }
}
