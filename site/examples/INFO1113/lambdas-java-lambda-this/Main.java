// Guoliang | Original learning example
// See which object this names
public class Main {
    static final class Presenter {
        private final String name = "outer";
        void show() {
            Runnable lambda = () -> System.out.println("lambda=" + this.name);
            Runnable anonymous = new Runnable() {
                private final String name = "inner";
                public void run() {
                    System.out.println("anonymous=" + this.name);
                    System.out.println("enclosing=" + Presenter.this.name);
                }
            };
            lambda.run();
            anonymous.run();
        }
    }
    public static void main(String[] args) {
        new Presenter().show();
    }
}
