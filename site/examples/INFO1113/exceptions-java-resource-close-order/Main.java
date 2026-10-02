// Guoliang | Original learning example
// Observe cleanup during exception propagation
public class Main {
    static final class Resource implements AutoCloseable {
        private final String name;
        Resource(String name) {
            this.name = name;
            System.out.println("open=" + name);
        }
        void use() {
            System.out.println("use=" + name);
        }
        @Override
        public void close() {
            System.out.println("close=" + name);
        }
    }
    public static void main(String[] args) {
        try (Resource first = new Resource("first");
             Resource second = new Resource("second")) {
            first.use();
            second.use();
            throw new IllegalStateException("work failed");
        } catch (IllegalStateException ex) {
            System.out.println("caught=" + ex.getMessage());
        }
        System.out.println("continued");
    }
}
