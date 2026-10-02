// Guoliang | Original learning example
// Separate type knowledge from mutability
import java.util.*;

public class Main {

    public static void main(String[] args) {
        List<Integer> numbers = new ArrayList<>(Arrays.asList(3, 7));
        List<? extends Number> source = numbers;
        Number first = source.get(0);
        source.remove(0);
        List<Object> mixed = new ArrayList<>();
        mixed.add("note");
        List<? super Integer> destination = mixed;
        destination.add(9);
        Object earlier = destination.get(0);
        System.out.println("read number=" + first);
        System.out.println("after removal=" + numbers);
        System.out.println("earlier=" + earlier);
        System.out.println("destination=" + mixed);
    }
}
