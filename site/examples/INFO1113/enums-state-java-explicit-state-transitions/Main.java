// Guoliang | Original learning example
// Accept and reject workflow events
public class Main {
    enum State { QUEUED, RUNNING, DONE }
    static State next(State state, String event) {
        if (state == State.QUEUED && event.equals("start"))
            return State.RUNNING;
        if (state == State.RUNNING && event.equals("finish"))
            return State.DONE;
        throw new IllegalStateException("invalid transition");
    }
    public static void main(String[] args) {
        State state = State.QUEUED;
        for (String event : new String[] {"start", "start", "finish", "start"}) {
            try {
                state = next(state, event);
                System.out.println(event + " -> " + state);
            } catch (IllegalStateException ex) {
                System.out.println(event + " rejected at " + state);
            }
        }
    }
}
