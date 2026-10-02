// Guoliang | Original learning example
// Resolve two interface defaults
public class Main {
    interface Description {
        String describe();
    }
    interface Left extends Description {
        default String describe() {
            return "left";
        }
        static String category() {
            return "description provider";
        }
    }
    interface Right extends Description {
        default String describe() {
            return "right";
        }
    }
    static final class Both implements Left, Right {
        @Override
        public String describe() {
            return Left.super.describe() + "+" + Right.super.describe();
        }
    }
    public static void main(String[] args) {
        Description item = new Both();
        System.out.println(item.describe());
        System.out.println(Left.category());
    }
}
