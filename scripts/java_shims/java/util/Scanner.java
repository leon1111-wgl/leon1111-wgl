package java.util;

import java.io.InputStream;

/** A small Scanner for the browser's Java class library, which has none. Text only; whitespace-separated tokens and lines. */
public final class Scanner implements AutoCloseable {
    public static String stdinText = "";
    private final String text;
    private int position;
    private boolean closed;

    public Scanner(InputStream in) {
        this(stdinText);
    }

    public Scanner(String source) {
        this.text = source;
    }

    private void open() {
        if (closed) {
            throw new IllegalStateException("Scanner closed");
        }
    }

    private int tokenStart() {
        int i = position;
        while (i < text.length() && Character.isWhitespace(text.charAt(i))) {
            i++;
        }
        return i;
    }

    public boolean hasNext() {
        open();
        return tokenStart() < text.length();
    }

    private String peek() {
        int start = tokenStart();
        int end = start;
        while (end < text.length() && !Character.isWhitespace(text.charAt(end))) {
            end++;
        }
        return text.substring(start, end);
    }

    public String next() {
        open();
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        int start = tokenStart();
        String token = peek();
        position = start + token.length();
        return token;
    }

    public boolean hasNextInt() {
        if (!hasNext()) {
            return false;
        }
        try {
            Integer.parseInt(peek());
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    public int nextInt() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        try {
            int result = Integer.parseInt(peek());
            next();
            return result;
        } catch (NumberFormatException e) {
            throw new InputMismatchException(peek());
        }
    }

    public long nextLong() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        try {
            long result = Long.parseLong(peek());
            next();
            return result;
        } catch (NumberFormatException e) {
            throw new InputMismatchException(peek());
        }
    }

    public boolean hasNextDouble() {
        if (!hasNext()) {
            return false;
        }
        try {
            Double.parseDouble(peek());
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    public double nextDouble() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        try {
            double result = Double.parseDouble(peek());
            next();
            return result;
        } catch (NumberFormatException e) {
            throw new InputMismatchException(peek());
        }
    }

    public boolean nextBoolean() {
        String token = peek();
        if (!token.equalsIgnoreCase("true") && !token.equalsIgnoreCase("false")) {
            throw new InputMismatchException(token);
        }
        next();
        return token.equalsIgnoreCase("true");
    }

    public boolean hasNextLine() {
        open();
        return position < text.length();
    }

    public String nextLine() {
        open();
        if (position >= text.length()) {
            throw new NoSuchElementException("No line found");
        }
        int end = text.indexOf('\n', position);
        String line;
        if (end < 0) {
            line = text.substring(position);
            position = text.length();
        } else {
            line = text.substring(position, end);
            position = end + 1;
        }
        if (line.endsWith("\r")) {
            line = line.substring(0, line.length() - 1);
        }
        return line;
    }

    @Override
    public void close() {
        closed = true;
    }
}
