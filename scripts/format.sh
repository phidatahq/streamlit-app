#!/bin/bash

############################################################################
#
# Run this script to format using ruff
# Usage:
#   ./scripts/format.sh
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname $CURR_DIR)"
source ${CURR_DIR}/_utils.sh

main() {
  print_heading "Formatting workspace..."
  print_heading "Running: ruff format ${REPO_ROOT}"
  ruff format ${REPO_ROOT}
}

main "$@"
