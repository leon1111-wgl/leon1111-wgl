// Leon | Original learning example
// Follow a command through a small application
public class Main {
    static final class Bed {
        private int moisture;
        Bed(int initial) {
            if (initial < 0 || initial > 10)
                throw new IllegalArgumentException("range");
            moisture = initial;
        }
        void water(int amount) {
            if (amount < 0 || amount > 10 - moisture)
                throw new IllegalArgumentException("range");
            moisture += amount;
        }
    }
    static String handle(Bed bed, String command) {
        String[] parts = command.split(" ");
        if (parts.length != 2 || !parts[0].equals("water"))
            return "unknown command";
        try {
            bed.water(Integer.parseInt(parts[1]));
            return "accepted";
        } catch (IllegalArgumentException ex) {
            return "rejected";
        }
    }
    static String render(Bed bed) {
        return "moisture=" + bed.moisture;
    }
    public static void main(String[] args) {
        Bed bed = new Bed(4);
        for (String command : new String[] {"water 2", "water 8", "water many"}) {
            System.out.println(command + " -> " + handle(bed, command));
            System.out.println(render(bed));
        }
    }
}
