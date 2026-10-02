// Guoliang | Original learning example
// Decode explicit enum codes
public class Main {
    enum Mode {
        IDLE(10),
        ACTIVE(20),
        STOPPED(30);
        private final int code;
        Mode(int code) {
            this.code = code;
        }
        int code() {
            return code;
        }
        static Mode fromCode(int code) {
            for (Mode mode : values())
                if (mode.code == code)
                    return mode;
            throw new IllegalArgumentException("unknown code");
        }
    }
    public static void main(String[] args) {
        for (Mode mode : Mode.values())
            System.out.println(mode + ": code=" + mode.code());
        System.out.println("decoded=" + Mode.fromCode(20));
        try {
            Mode.fromCode(99);
        } catch (IllegalArgumentException ex) {
            System.out.println("unknown code rejected");
        }
    }
}
