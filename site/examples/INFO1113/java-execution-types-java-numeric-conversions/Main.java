// Guoliang | Original learning example
// Observe when conversion happens
public class Main {

    public static void main(String[] args) {
        int trips = 7, days = 2;
        double late = trips / days;
        double early = (double)trips / days;
        int width = 50000;
        long area = (long)width * width;
        System.out.println("late=" + late);
        System.out.println("early=" + early);
        System.out.println("area=" + area);
        System.out.println("truncate=" + (int)-3.9);
    }
}
