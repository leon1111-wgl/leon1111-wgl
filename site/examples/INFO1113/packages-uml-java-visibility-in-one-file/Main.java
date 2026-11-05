// Leon | Original learning example
// Visibility inside one file, and the full rule table
/** Not public, so it is package-private: only classes in this package can see the class itself. */
class Vault {
    private int secret = 7;
    int packageLevel = 1;
    protected int shared = 2;
    public int open = 3;

    int reveal() {
        return secret;
    }
}

/** A subclass. Inside one package it can use protected and package-level members. */
class Safe extends Vault {
    int total() {
        return shared + packageLevel + open;
    }

    // int bad() { return secret; }   // error: secret has private access in Vault
}

public class Main {
    /** Nested classes share their private members with the enclosing top-level class. */
    static class Counter {
        private int hidden = 5;
    }

    static final int CLASS = 1, PACKAGE = 2, SUBCLASS = 4, ANYONE = 8;

    /** Who may use a member declared with each modifier (JLS 6.6), as a set of places. */
    static int places(String modifier) {
        switch (modifier) {
            case "private":
                return CLASS;
            case "(none)":
                return CLASS | PACKAGE;
            case "protected":
                return CLASS | PACKAGE | SUBCLASS;
            default:
                return CLASS | PACKAGE | SUBCLASS | ANYONE;
        }
    }

    static String yesNo(int set, int place) {
        return (set & place) != 0 ? "yes" : "no";
    }

    public static void main(String[] args) {
        Vault vault = new Vault();
        Safe safe = new Safe();
        System.out.println("same package, package-private field: " + vault.packageLevel);
        System.out.println("same package, protected field: " + vault.shared);
        System.out.println("private field through a method: " + vault.reveal());
        // System.out.println(vault.secret);   // error: secret has private access in Vault
        System.out.println("subclass uses inherited members: " + safe.total());
        System.out.println("nested private seen by the outer class: " + new Counter().hidden);

        System.out.println();
        System.out.println("modifier   same class  same package  subclass elsewhere  anyone");
        String[] modifiers = {"private", "(none)", "protected", "public"};
        for (String modifier : modifiers) {
            int set = places(modifier);
            System.out.println(String.format("%-10s %-11s %-13s %-19s %s", modifier,
                    yesNo(set, CLASS), yesNo(set, PACKAGE), yesNo(set, SUBCLASS), yesNo(set, ANYONE)));
        }
    }
}
