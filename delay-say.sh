#!/bin/bash

# Default delay is 1 second
DELAY=1

# Parse options
while [[ "$1" == -* ]]; do
  case "$1" in
    -d)
      DELAY="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      echo "Usage: $0 [-d delay_in_seconds] -- [say_options]" >&2
      exit 1
      ;;
  esac
done

# Read input from stdin, handling the lack of a newline at the end
input=$(cat)
for word in $input; do
  echo "$word"
  echo "$word" | say "$@"
  sleep "$DELAY"
done