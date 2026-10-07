// Leon | Original learning example
// Inject a recording collaborator
import java.util.*;

public class Main {
    interface Sink {
        void send(String text);
    }
    static final class RecordingSink implements Sink {
        final List<String> messages = new ArrayList<>();
        public void send(String text) {
            messages.add(Objects.requireNonNull(text));
        }
    }
    static final class Reporter {
        private final Sink sink;
        Reporter(Sink sink) {
            this.sink = Objects.requireNonNull(sink);
        }
        void sendAll(List<String> messages) {
            for (String message : messages)
                sink.send(message);
        }
    }
    public static void main(String[] args) {
        RecordingSink sink = new RecordingSink();
        Reporter reporter = new Reporter(sink);
        reporter.sendAll(Arrays.asList("ready", "running", "done"));
        System.out.println(sink.messages);
    }
}
