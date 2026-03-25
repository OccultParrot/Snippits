#!/usr/bin/env bash
# Common Bash utility functions.
# Source this file in your scripts: source ./bash_utils.sh

# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RESET='\033[0m'

log_info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
log_success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*" >&2; }
log_error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; }

# ---------------------------------------------------------------------------
# Guard / assertion helpers
# ---------------------------------------------------------------------------

# Exit with an error message if a required environment variable is unset.
# Usage: require_env MY_SECRET DB_PASSWORD
require_env() {
    for var in "$@"; do
        if [[ -z "${!var:-}" ]]; then
            log_error "Required environment variable '$var' is not set."
            exit 1
        fi
    done
}

# Exit with an error message if a command is not found on PATH.
# Usage: require_cmd git curl jq
require_cmd() {
    for cmd in "$@"; do
        if ! command -v "$cmd" &>/dev/null; then
            log_error "Required command '$cmd' not found. Please install it."
            exit 1
        fi
    done
}

# ---------------------------------------------------------------------------
# String helpers
# ---------------------------------------------------------------------------

# Convert a string to lower-case.
to_lower() { echo "$*" | tr '[:upper:]' '[:lower:]'; }

# Convert a string to upper-case.
to_upper() { echo "$*" | tr '[:lower:]' '[:upper:]'; }

# Trim leading and trailing whitespace from a string.
trim() {
    local s="$*"
    s="${s#"${s%%[![:space:]]*}"}"
    s="${s%"${s##*[![:space:]]}"}"
    echo "$s"
}

# Check whether a string contains a substring.
# Usage: if contains "hello world" "world"; then ...
contains() {
    [[ "$1" == *"$2"* ]]
}

# ---------------------------------------------------------------------------
# File / directory helpers
# ---------------------------------------------------------------------------

# Create a directory (including parents) only if it does not already exist.
ensure_dir() {
    [[ -d "$1" ]] || mkdir -p "$1"
}

# Safely delete a file or directory; silently succeeds if it does not exist.
safe_remove() {
    if [[ -d "$1" ]]; then
        rm -rf "$1"
    elif [[ -e "$1" ]]; then
        rm -f "$1"
    fi
}

# Return the absolute path of a file (without requiring the file to exist).
abspath() {
    python3 -c "import os, sys; print(os.path.abspath(sys.argv[1]))" "$1"
}

# ---------------------------------------------------------------------------
# Process helpers
# ---------------------------------------------------------------------------

# Retry a command up to N times with a delay between attempts.
# Usage: retry 3 2 curl -f https://example.com
retry() {
    local max_attempts="$1"
    local delay="$2"
    shift 2
    local attempt=1
    until "$@"; do
        if (( attempt >= max_attempts )); then
            log_error "Command failed after $max_attempts attempts: $*"
            return 1
        fi
        log_warn "Attempt $attempt/$max_attempts failed. Retrying in ${delay}s..."
        sleep "$delay"
        (( attempt++ ))
    done
}

# Run a command and measure its wall-clock time.
# Usage: time_cmd sleep 2
time_cmd() {
    local start end elapsed
    start=$(date +%s%N)
    "$@"
    local status=$?
    end=$(date +%s%N)
    elapsed=$(( (end - start) / 1000000 ))
    log_info "'$*' completed in ${elapsed}ms"
    return $status
}

# ---------------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------------

# Ask the user a yes/no question; returns 0 for yes, 1 for no.
# Usage: if confirm "Delete all files?"; then rm -rf ...; fi
confirm() {
    local prompt="${1:-Are you sure?} [y/N] "
    read -r -p "$prompt" answer
    case "$(to_lower "$answer")" in
        y|yes) return 0 ;;
        *)     return 1 ;;
    esac
}

# Generate a random alphanumeric string of a given length (default: 16).
# Usage: token=$(random_string 32)
random_string() {
    local length="${1:-16}"
    LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c "$length"
}

# Print a horizontal rule of a given width (default: 60).
hr() {
    printf '%*s\n' "${1:-60}" '' | tr ' ' '-'
}
