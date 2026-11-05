"""Print JaCoCo totals and every source line the tests missed.

usage: python3 uncovered.py report.xml src
"""
import sys
import xml.etree.ElementTree as ET


def main(report, srcdir):
    root = ET.parse(report).getroot()
    for kind in ("INSTRUCTION", "LINE", "BRANCH"):
        counter = [c for c in root.findall("counter") if c.get("type") == kind]
        missed = int(counter[0].get("missed")) if counter else 0
        covered = int(counter[0].get("covered")) if counter else 0
        total = missed + covered
        percent = 100.0 * covered / total if total else 100.0
        print("%-12s %3d of %3d covered (%3.0f%%)" % (kind.lower(), covered, total, percent))

    found = False
    for package in root.findall("package"):
        for sourcefile in package.findall("sourcefile"):
            path = "%s/%s/%s" % (srcdir, package.get("name"), sourcefile.get("name"))
            with open(path) as handle:
                text = handle.read().split("\n")
            for line in sourcefile.findall("line"):
                nr = int(line.get("nr"))
                missed_instr = int(line.get("mi"))
                covered_instr = int(line.get("ci"))
                missed_branch = int(line.get("mb"))
                covered_branch = int(line.get("cb"))
                if missed_instr == 0 and missed_branch == 0:
                    continue
                found = True
                if covered_instr == 0:
                    note = "never executed"
                else:
                    note = "%d of %d branches missed" % (missed_branch, missed_branch + covered_branch)
                print("%s:%d  %-24s %s" % (sourcefile.get("name"), nr, note, text[nr - 1].strip()))
    if not found:
        print("nothing missed: every line and branch was executed")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
