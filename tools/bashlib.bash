# Library of Bash utilities
#
# https://google.github.io/styleguide/shellguide.html

# http://mywiki.wooledge.org/BashFAQ/037
BOLD=$(tput bold)
CYAN=$(tput setaf 6)
RED=$(tput setaf 1)
RESET=$(tput sgr0)
# shellcheck disable=SC2034
readonly BOLD CYAN YELLOW RED RESET


# Print a message to stderr.
# Arguments:
#   An error message.
# Outputs:
#   Writes the message to stderr.
bashlib::err() {
  echo "${*}" >&2
}


# Ask for input until 'y' or 'n' (i.e. yes or no) is received.
# Arguments:
#   A prompt text.
# Outputs:
#   Writes the prompt to stdout if the input is coming from a terminal. Reads
#   the answer from stdin.
# Returns:
#   0 if received a positive answer, 1 otherwise.
bashlib::ask() {
  while true; do
    # shellcheck disable=SC2162
    read -p "$* [y/n]: " answer
    case "${answer}" in
      y) return 0;;
      n) return 1;;
      *) bashlib::err "Invalid input. Answer 'y' or 'n'.";;
    esac
  done
}


# Ask for confirmation to execute a command. Compound commands must be
# enclosed in parentheses (e.g. 'cd /path/to/directory && ls').
# Arguments:
#   A command to run.
# Outputs:
#   Writes the command to stdout if the input is coming from a terminal.
#   Reads the confirmation from stdin.
bashlib::confirm_cmd() {
    echo
    echo "${BOLD}${1}${RESET}"
    if bashlib::ask "Execute?"; then
        eval "${1}"
    fi
}
