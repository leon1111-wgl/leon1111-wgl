// Leon | Original learning example
// Separate class methods from instance methods
public class Main {
    static class Base {
        static String kind() {
            return "base kind";
        }
        String describe() {
            return "base instance";
        }
        Object label() {
            return "base label";
        }
    }
    static final class Derived extends Base {
        static String kind() {
            return "derived kind";
        }
        @Override
        String describe() {
            return "derived instance";
        }
        @Override
        String label() {
            return "derived label";
        }
    }
    public static void main(String[] args) {
        Base value = new Derived();
        System.out.println("base static=" + Base.kind());
        System.out.println("derived static=" + Derived.kind());
        System.out.println("instance=" + value.describe());
        System.out.println("covariant value=" + value.label());
    }
}
