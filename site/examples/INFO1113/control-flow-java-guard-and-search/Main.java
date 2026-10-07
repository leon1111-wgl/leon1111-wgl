// Leon | Original learning example
// Guard null and stop at the first match
public class Main {

    public static void main(String[] args) {
        String[] names = {null, "", "oak", "pine", "elm"};
        int found = -1;
        for (int i = 0; i < names.length; i++) {
            String name = names[i];
            if (name == null || name.isEmpty())
                continue;
            if (name.length() == 4) {
                found = i;
                break;
            }
        }
        System.out.println("first length-four index=" + found);
        System.out.println("matched=" + names[found]);
    }
}
