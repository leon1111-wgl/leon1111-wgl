// Guoliang | Original learning example
// Capture a threshold and a mutable log
public class Main {

    public static void main(String[] args) {
        int threshold = 3;
        java.util.function.Predicate<String> longEnough = s -> s.length() >= threshold;
        java.util.List<String> log = new java.util.ArrayList<>();
        Runnable report = () -> System.out.println("log size=" + log.size());
        System.out.println("oak accepted=" + longEnough.test("oak"));
        System.out.println("ox accepted=" + longEnough.test("ox"));
        report.run();
        log.add("visited");
        report.run();
    }
}
