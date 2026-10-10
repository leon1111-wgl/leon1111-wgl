// Leon | Original learning example
// Use a value object as a map key
import java.util.HashMap;
import java.util.Map;
public class Main {
    static final class Cell {
        private final int row;
        private final int column;
        Cell(int row, int column) { this.row = row; this.column = column; }
        @Override public boolean equals(Object other) {
            if (this == other) return true;
            if (!(other instanceof Cell)) return false;
            Cell cell = (Cell) other;
            return row == cell.row && column == cell.column;
        }
        @Override public int hashCode() { return 31 * row + column; }
    }
    public static void main(String[] args) {
        Cell a = new Cell(2, 3);
        Cell b = new Cell(2, 3);
        Cell collision = new Cell(1, 34);
        Map<Cell, String> notes = new HashMap<>();
        notes.put(a, "charging");
        notes.put(collision, "door");
        assert a != b && a.equals(b) && b.equals(a);
        assert a.hashCode() == collision.hashCode();
        assert !a.equals(collision) && !a.equals(null);
        assert "charging".equals(notes.get(b));
        System.out.println("same object: " + (a == b));
        System.out.println("same value: " + a.equals(b));
        System.out.println("lookup: " + notes.get(b));
        System.out.println("collision keeps both: " + notes.size());
    }
}
