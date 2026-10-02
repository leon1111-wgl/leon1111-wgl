// Guoliang | Original learning example
// Share construction while requiring behavior
public class Main {
    static abstract class Shape {
        private final String name;
        Shape(String name) {
            this.name = java.util.Objects.requireNonNull(name);
        }
        abstract int area();
        String describe() {
            return name + ": area=" + area();
        }
    }
    static final class Rectangle extends Shape {
        private final int width, height;
        Rectangle(String name, int width, int height) {
            super(name);
            if (width <= 0 || height <= 0)
                throw new IllegalArgumentException();
            this.width = width;
            this.height = height;
        }
        @Override
        int area() {
            return Math.multiplyExact(width, height);
        }
    }
    public static void main(String[] args) {
        Shape shape = new Rectangle("panel", 3, 4);
        System.out.println(shape.describe());
    }
}
