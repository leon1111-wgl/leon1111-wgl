// Leon | Original learning example
// From a design to a class diagram and Javadoc
import java.util.ArrayList;
import java.util.List;

/**
 * Something that can describe itself in one line.
 *
 * @since 1.0
 */
interface Describable {
    /**
     * Builds the description.
     *
     * @return a one-line description, never {@code null}
     */
    String describe();
}

/**
 * A flat shape with a whole-number area.
 *
 * <p>Subclasses supply {@link #area()}; the description is built here once.
 *
 * @see Rect
 * @see Triangle
 */
abstract class Shape implements Describable {
    private final String name;

    /**
     * Creates a shape.
     *
     * @param name the label used in descriptions, not {@code null}
     */
    protected Shape(String name) {
        this.name = name;
    }

    /**
     * Computes the area.
     *
     * @return the area in square units, never negative
     */
    public abstract int area();

    @Override
    public String describe() {
        return name + " area=" + area();
    }
}

/** A rectangle. */
class Rect extends Shape {
    private final int width;
    private final int height;

    /**
     * Creates a rectangle.
     *
     * @param width  the width in units, at least 1
     * @param height the height in units, at least 1
     * @throws IllegalArgumentException if either side is less than 1
     */
    Rect(int width, int height) {
        this("rect", width, height);
    }

    /**
     * Lets a subclass choose its own label.
     *
     * @param name   the label used in descriptions
     * @param width  the width in units, at least 1
     * @param height the height in units, at least 1
     */
    protected Rect(String name, int width, int height) {
        super(name);
        if (width < 1 || height < 1) {
            throw new IllegalArgumentException("sides must be at least 1");
        }
        this.width = width;
        this.height = height;
    }

    @Override
    public int area() {
        return width * height;
    }
}

/** A square is a rectangle whose sides match. */
class Square extends Rect {
    Square(int side) {
        super("square", side, side);
    }
}

/** A triangle given by its base and height. */
class Triangle extends Shape {
    private final int base;
    private final int height;

    Triangle(int base, int height) {
        super("triangle");
        this.base = base;
        this.height = height;
    }

    @Override
    public int area() {
        return base * height / 2;
    }
}

/**
 * A list of shapes of one kind.
 *
 * @param <T> the kind of shape stored; a Catalog&lt;Rect&gt; holds only rectangles
 */
class Catalog<T extends Shape> {
    private final List<T> items = new ArrayList<T>();

    /**
     * Adds an item.
     *
     * @param item the shape to store
     */
    void add(T item) {
        items.add(item);
    }

    /**
     * Finds the item with the largest area.
     *
     * @return the largest item, or {@code null} when the catalog is empty
     */
    T largest() {
        T best = null;
        for (T item : items) {
            if (best == null || item.area() > best.area()) {
                best = item;
            }
        }
        return best;
    }

    int size() {
        return items.size();
    }
}

public class Main {
    public static void main(String[] args) {
        Catalog<Shape> shapes = new Catalog<Shape>();
        shapes.add(new Rect(3, 4));
        shapes.add(new Triangle(6, 5));
        shapes.add(new Square(4));
        System.out.println("catalog holds " + shapes.size() + " shapes");
        System.out.println("largest: " + shapes.largest().describe());

        Catalog<Rect> rects = new Catalog<Rect>();
        rects.add(new Rect(2, 9));
        rects.add(new Square(3));
        Rect widest = rects.largest();
        System.out.println("largest rect: " + widest.describe());

        Describable d = new Square(5);
        System.out.println("through the interface: " + d.describe());
        try {
            new Rect(0, 3);
        } catch (IllegalArgumentException ex) {
            System.out.println("rejected: " + ex.getMessage());
        }
        Catalog<Triangle> empty = new Catalog<Triangle>();
        System.out.println("empty catalog largest: " + empty.largest());
    }
}
