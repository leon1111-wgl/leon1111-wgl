// Leon | Original learning example
// Keep unequal colliding keys distinct
import java.util.*;

public class Main {
    static final class Key {
        private final int id;
        Key(int id) {
            this.id = id;
        }
        @Override
        public boolean equals(Object other) {
            return other instanceof Key && id == ((Key)other).id;
        }
        @Override
        public int hashCode() {
            return 42;
        }
    }
    public static void main(String[] args) {
        Map<Key, String> values = new HashMap<>();
        values.put(new Key(1), "north");
        values.put(new Key(2), "south");
        values.put(new Key(1), "updated");
        System.out.println("keys=" + values.size());
        System.out.println("key 1=" + values.get(new Key(1)));
        System.out.println("key 2=" + values.get(new Key(2)));
        System.out.println("same hash=" +
                           (new Key(1).hashCode() == new Key(2).hashCode()));
    }
}
