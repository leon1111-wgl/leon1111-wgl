// Leon | Original learning example
// Build labels and count Unicode units
public class Main {

    public static void main(String[] args) {
        StringBuilder builder = new StringBuilder();
        for (int day = 1; day <= 3; day++) {
            if (day > 1)
                builder.append(", ");
            builder.append("Day ").append(day);
        }
        System.out.println(builder.toString());
        String symbol = new String(Character.toChars(0x1F680));
        System.out.println("code units=" + symbol.length());
        System.out.println("code points=" + symbol.codePointCount(0, symbol.length()));
    }
}
