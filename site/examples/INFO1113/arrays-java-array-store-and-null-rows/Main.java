// Guoliang | Original learning example
// Handle null rows and checked stores
public class Main {

    public static void main(String[] args) {
        int[][] rows = {{1, 2}, null, {}, {3}};
        int cells = 0;
        for (int[] row : rows)
            if (row != null)
                cells += row.length;
        System.out.println("cells=" + cells);
        Object[] values = new String[2];
        values[0] = "safe";
        try {
            values[1] = Integer.valueOf(5);
        } catch (ArrayStoreException ex) {
            System.out.println("incompatible store rejected");
        }
        System.out.println("second slot=" + values[1]);
    }
}
