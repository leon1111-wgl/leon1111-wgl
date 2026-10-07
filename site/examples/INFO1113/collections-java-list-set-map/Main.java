// Leon | Original learning example
// Represent events, uniqueness, and counts
import java.util.*;

public class Main {

    public static void main(String[] args) {
        List<String> arrivals = Arrays.asList("Mia", "Leo", "Mia");
        Set<String> unique = new HashSet<>(arrivals);
        Map<String, Integer> counts = new LinkedHashMap<>();
        for (String name : arrivals)
            counts.put(name, counts.getOrDefault(name, 0) + 1);
        System.out.println("events=" + arrivals);
        System.out.println("unique count=" + unique.size());
        System.out.println("counts=" + counts);
        counts.put("Mia", 3);
        System.out.println("after replacement=" + counts + ", keys=" + counts.size());
    }
}
