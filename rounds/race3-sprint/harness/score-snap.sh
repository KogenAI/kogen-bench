#!/bin/bash
# score-snap.sh LABEL — score all 4 arms of a snapshot IN PARALLEL (one scorer per arm), wait for all
R=~/Scratch.noindex/race2s; for A in $(cat ~/Scratch.noindex/race2s/ARMS); do $R/score-arm.sh "$1" $A & done; wait
