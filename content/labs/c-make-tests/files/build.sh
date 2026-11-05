#!/bin/sh
# How the team builds today: every file, every time, with no warnings.
cc -o sampler main.c ring.c stats.c util.c
cc -o test_ring test_ring.c ring.c stats.c util.c
