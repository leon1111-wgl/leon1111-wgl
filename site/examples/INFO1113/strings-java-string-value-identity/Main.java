// Leon | Original learning example
// Separate text value from object identity
public class Main {

    public static void main(String[] args) {
        String a = new String("harbor");
        String b = new String("harbor");
        System.out.println("identity=" + (a == b));
        System.out.println("content=" + a.equals(b));
        a.toUpperCase(java.util.Locale.ROOT);
        System.out.println("ignored result=" + a);
        a = a.toUpperCase(java.util.Locale.ROOT);
        System.out.println("assigned result=" + a);
    }
}
