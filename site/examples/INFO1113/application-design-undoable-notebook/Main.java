// Leon | Original learning example
// Build a small editor with undo
import java.util.ArrayDeque;
import java.util.Deque;
public class Main {
    interface Edit { String apply(String text); }
    static final class Append implements Edit {
        private final String suffix;
        Append(String suffix) { this.suffix = suffix; }
        @Override public String apply(String text) {
            if (suffix == null || suffix.isEmpty())
                throw new IllegalArgumentException("empty edit");
            return text + suffix;
        }
    }
    static final class Editor {
        private String text = "";
        private final Deque<String> history = new ArrayDeque<>();
        void execute(Edit edit) {
            String next = edit.apply(text);
            if (next == null) throw new IllegalArgumentException("null result");
            history.push(text);
            text = next;
        }
        boolean undo() {
            if (history.isEmpty()) return false;
            text = history.pop();
            return true;
        }
        String text() { return text; }
    }
    public static void main(String[] args) {
        Editor editor = new Editor();
        assert !editor.undo();
        editor.execute(new Append("Hello"));
        editor.execute(new Append(" Python"));
        System.out.println(editor.text());
        try { editor.execute(new Append("")); }
        catch (IllegalArgumentException error) { System.out.println("rejected without history"); }
        if (!editor.undo()) throw new AssertionError("missing history");
        assert editor.text().equals("Hello");
        System.out.println("undo: " + editor.text());
    }
}
