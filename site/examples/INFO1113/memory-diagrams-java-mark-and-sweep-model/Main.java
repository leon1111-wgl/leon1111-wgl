// Leon | Original learning example
// Run mark-and-sweep on a tiny heap
import java.util.ArrayList;
import java.util.List;

public class Main {
    /** One heap object with up to two outgoing references. */
    static final class Obj {
        final String name;
        Obj left;
        Obj right;
        boolean marked;

        Obj(String name) {
            this.name = name;
        }
    }

    /** A model of the heap: it knows every object, so it can sweep. */
    static final class Heap {
        final List<Obj> all = new ArrayList<Obj>();

        Obj alloc(String name) {
            Obj o = new Obj(name);
            all.add(o);
            return o;
        }

        /** Mark: follow references from a root, flagging everything reached. */
        void mark(Obj o, StringBuilder order) {
            if (o == null || o.marked) {
                return;
            }
            o.marked = true;
            order.append(o.name).append(' ');
            mark(o.left, order);
            mark(o.right, order);
        }

        /** Sweep: drop every unmarked object, then clear the marks for next time. */
        String sweep() {
            StringBuilder freed = new StringBuilder();
            List<Obj> kept = new ArrayList<Obj>();
            for (Obj o : all) {
                if (o.marked) {
                    o.marked = false;
                    kept.add(o);
                } else {
                    freed.append(o.name).append(' ');
                }
            }
            all.clear();
            all.addAll(kept);
            return freed.toString().trim();
        }

        void collect(String title, Obj... roots) {
            StringBuilder order = new StringBuilder();
            for (Obj root : roots) {
                mark(root, order);
            }
            String freed = sweep();
            System.out.println(title);
            System.out.println("  marked in order: " + order.toString().trim());
            System.out.println("  freed: " + (freed.isEmpty() ? "nothing" : freed));
            System.out.println("  heap now has " + all.size() + " objects");
        }
    }

    /** A diamond: A refers to B and C, and both refer to D. Only A is returned. */
    static Obj buildDiamond(Heap heap) {
        Obj a = heap.alloc("A");
        Obj b = heap.alloc("B");
        Obj c = heap.alloc("C");
        Obj d = heap.alloc("D");
        a.left = b;
        a.right = c;
        b.left = d;
        c.left = d;
        return a;
    }

    /** A cycle: E and F refer to each other. */
    static Obj buildCycle(Heap heap) {
        Obj e = heap.alloc("E");
        Obj f = heap.alloc("F");
        e.left = f;
        f.left = e;
        return e;
    }

    /** Its local variables vanish on return, so nothing can reach these objects. */
    static void leaveGarbage(Heap heap) {
        heap.alloc("G");
        Obj h = heap.alloc("H");
        Obj i = heap.alloc("I");
        h.left = i;
        i.left = h;
    }

    public static void main(String[] args) {
        Heap heap = new Heap();
        Obj a = buildDiamond(heap);
        Obj e = buildCycle(heap);
        leaveGarbage(heap);
        System.out.println("heap starts with " + heap.all.size() + " objects");
        System.out.println("roots are variables a and e; G and the H-I pair are unreachable");

        heap.collect("collection 1", a, e);

        e = null;
        heap.collect("collection 2 after e = null", a);

        a.right = null;
        heap.collect("collection 3 after a.right = null", a);
    }
}
