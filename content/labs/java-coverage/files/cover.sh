#!/bin/sh
# Run the tests under the JaCoCo agent, write the reports, and list what was missed.
# Expects the classes in out/main and out/test, and $LAB_TOOLS set.
set -e
rm -f jacoco.exec
java "-javaagent:$LAB_TOOLS/jacocoagent.jar=destfile=jacoco.exec,includes=shop.*" \
     -jar $LAB_TOOLS/junit.jar execute --class-path out/main:out/test \
     --select-class shop.InventoryTest --disable-banner --disable-ansi-colors --details=summary
java -jar $LAB_TOOLS/jacococli.jar report jacoco.exec --classfiles out/main --sourcefiles src \
     --csv report.csv --xml report.xml --html report-html > /dev/null
python3 uncovered.py report.xml src
