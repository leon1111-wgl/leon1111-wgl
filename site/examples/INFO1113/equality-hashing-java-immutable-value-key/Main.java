// Guoliang | Original learning example
// Use immutable seats as value keys
import java.util.*;

public class Main {
    static final class Seat {
        private final String row;
        private final int number;
        Seat(String row, int number) {
            this.row = Objects.requireNonNull(row);
            this.number = number;
        }
        @Override
        public boolean equals(Object other) {
            if (this == other)
                return true;
            if (!(other instanceof Seat))
                return false;
            Seat seat = (Seat)other;
            return number == seat.number && row.equals(seat.row);
        }
        @Override
        public int hashCode() {
            return Objects.hash(row, number);
        }
    }
    public static void main(String[] args) {
        Seat a = new Seat("B", 7), b = new Seat("B", 7);
        Set<Seat> seats = new HashSet<>();
        seats.add(a);
        seats.add(b);
        seats.add(new Seat("B", 8));
        System.out.println("identity=" + (a == b));
        System.out.println("equal=" + a.equals(b));
        System.out.println("equal hashes=" + (a.hashCode() == b.hashCode()));
        System.out.println("logical seats=" + seats.size());
    }
}
