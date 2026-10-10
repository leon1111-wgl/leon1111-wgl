// Leon | Original learning example
// Protect a score snapshot from outside changes
import java.util.Arrays;
public class Main {
    static final class ScoreSnapshot {
        private final int[] scores;
        ScoreSnapshot(int[] source) {
            if (source == null) throw new IllegalArgumentException("missing scores");
            int[] copy = source.clone();
            for (int score : copy) {
                if (score < 0 || score > 100)
                    throw new IllegalArgumentException("score out of range");
            }
            scores = copy;
        }
        int[] values() { return scores.clone(); }
        int total() {
            int sum = 0;
            for (int score : scores) sum = Math.addExact(sum, score);
            return sum;
        }
    }
    public static void main(String[] args) {
        int[] input = {70, 80, 90};
        ScoreSnapshot report = new ScoreSnapshot(input);
        input[0] = 0;
        int[] exported = report.values();
        exported[1] = 0;
        assert report.total() == 240;
        System.out.println("snapshot: " + Arrays.toString(report.values()));
        System.out.println("total: " + report.total());
        try { new ScoreSnapshot(new int[]{101}); }
        catch (IllegalArgumentException error) { System.out.println("invalid score rejected"); }
        assert new ScoreSnapshot(new int[0]).total() == 0;
    }
}
