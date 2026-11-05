#!/usr/bin/env bash
# The Java test and coverage tools the labs use, pinned, from Maven Central.
set -euo pipefail
mkdir -p "$1"
base=https://repo1.maven.org/maven2
curl -fsSL "$base/org/junit/platform/junit-platform-console-standalone/1.13.4/junit-platform-console-standalone-1.13.4.jar" -o "$1/junit.jar"
curl -fsSL "$base/org/jacoco/org.jacoco.agent/0.8.13/org.jacoco.agent-0.8.13-runtime.jar" -o "$1/jacocoagent.jar"
curl -fsSL "$base/org/jacoco/org.jacoco.cli/0.8.13/org.jacoco.cli-0.8.13-nodeps.jar" -o "$1/jacococli.jar"
