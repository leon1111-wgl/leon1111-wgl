// Leon | Original learning example
// Give each traversal its own cursor
import java.util.*;

public class Main {

    public static void main(String[] args) {
        List<String> trees = Arrays.asList("oak", "pine", "elm");
        Iterator<String> a = trees.iterator(), b = trees.iterator();
        System.out.println("a=" + a.next());
        System.out.println("a=" + a.next());
        System.out.println("b=" + b.next());
        System.out.println("a=" + a.next());
        System.out.println("a has next=" + a.hasNext());
        try {
            a.next();
        } catch (NoSuchElementException ex) {
            System.out.println("a exhausted");
        }
        System.out.println("b=" + b.next());
    }
}
