// Guoliang | Original learning example
// Contrast FIFO and LIFO with a deque
import java.util.*;

public class Main {

    public static void main(String[] args) {
        Deque<String> queue = new ArrayDeque<>();
        queue.addLast("oak");
        queue.addLast("pine");
        queue.addLast("elm");
        StringJoiner fifo = new StringJoiner(", ");
        while (!queue.isEmpty())
            fifo.add(queue.removeFirst());
        Deque<String> stack = new ArrayDeque<>();
        stack.push("oak");
        stack.push("pine");
        stack.push("elm");
        StringJoiner lifo = new StringJoiner(", ");
        while (!stack.isEmpty())
            lifo.add(stack.pop());
        System.out.println("FIFO=" + fifo);
        System.out.println("LIFO=" + lifo);
        System.out.println("empty poll=" + queue.pollFirst());
    }
}
