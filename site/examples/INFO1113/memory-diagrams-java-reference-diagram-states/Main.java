// Leon | Original learning example
// Print the diagram: primitives, references and arrays
public class Main {
    static int nextId = 1;

    /** A tiny object: it lives on the heap and has a label like an address. */
    static final class Box {
        final int id = nextId++;
        int value;

        Box(int value) {
            this.value = value;
        }

        String show() {
            return "#" + id + "{value=" + value + "}";
        }
    }

    static void change(int n, Box b, int[] a) {
        n = n + 1;
        b.value = b.value + 1;
        a[0] = 99;
        b = new Box(-1);
        System.out.println("inside change: n=" + n + " b=" + b.show() + " a[0]=" + a[0]);
    }

    public static void main(String[] args) {
        int n = 5;
        int m = n;
        m = 9;
        System.out.println("primitives: n=" + n + " m=" + m);

        Box p = new Box(3);
        Box q = p;
        Box r = new Box(3);
        System.out.println("p -> " + p.show() + ", q -> " + q.show() + ", r -> " + r.show());
        System.out.println("p == q: " + (p == q) + ", p == r: " + (p == r));

        q.value = 7;
        System.out.println("after q.value = 7: p -> " + p.show() + ", r -> " + r.show());
        q = new Box(1);
        System.out.println("after q = new Box(1): p -> " + p.show() + ", q -> " + q.show());

        int[] x = {1, 2};
        int[] y = x;
        y[1] = 20;
        System.out.println("x[1]=" + x[1] + " y[1]=" + y[1] + " same array: " + (x == y));

        Box[] row = new Box[3];
        row[0] = p;
        row[1] = r;
        System.out.println("row[0] -> " + row[0].show() + ", row[1] -> " + row[1].show()
                + ", row[2] -> " + row[2]);

        change(n, p, x);
        System.out.println("after change: n=" + n + " p -> " + p.show() + " x[0]=" + x[0]);
        System.out.println("row[0] sees it too: " + row[0].show());
    }
}
