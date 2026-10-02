// Guoliang | Original learning example
// Copy from a producer into a consumer
import java.util.*;

public class Main {
    static <T> void copy(List<? extends T> source, List<? super T> destination) {
        for (T value : source)
            destination.add(value);
    }
    public static void main(String[] args) {
        List<Integer> source = Arrays.asList(3, 7);
        List<Number> destination = new ArrayList<>();
        destination.add(2.5);
        copy(source, destination);
        System.out.println("source=" + source);
        System.out.println("destination=" + destination);
    }
}
