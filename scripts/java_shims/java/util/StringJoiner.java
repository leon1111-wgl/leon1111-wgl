package java.util;

/** A small StringJoiner for the browser's Java class library, which has none. */
public final class StringJoiner {
    private final String separator;
    private final String prefix;
    private final String suffix;
    private StringBuilder value;
    private String emptyValue;

    public StringJoiner(CharSequence separator) {
        this(separator, "", "");
    }

    public StringJoiner(CharSequence separator, CharSequence prefix, CharSequence suffix) {
        this.separator = separator.toString();
        this.prefix = prefix.toString();
        this.suffix = suffix.toString();
    }

    public StringJoiner setEmptyValue(CharSequence emptyValue) {
        this.emptyValue = emptyValue.toString();
        return this;
    }

    public StringJoiner add(CharSequence item) {
        if (value == null) {
            value = new StringBuilder();
        } else {
            value.append(separator);
        }
        value.append(String.valueOf(item));
        return this;
    }

    public int length() {
        return toString().length();
    }

    @Override
    public String toString() {
        if (value == null && emptyValue != null) {
            return emptyValue;
        }
        return prefix + (value == null ? "" : value.toString()) + suffix;
    }
}
