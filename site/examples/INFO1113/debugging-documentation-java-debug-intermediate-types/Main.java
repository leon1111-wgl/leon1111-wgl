// Leon | Original learning example
// Locate the first wrong intermediate value
public class Main {

    public static void main(String[] args) {
        int sum = 9, count = 2;
        int quotient = sum / count;
        double late = (double)quotient;
        double early = (double)sum / count;
        System.out.println("integer quotient=" + quotient);
        System.out.println("late conversion=" + late);
        System.out.println("early conversion=" + early);
        if (early != 4.5)
            throw new AssertionError("fraction lost");
    }
}
