# Raise the open-file descriptor soft limit.
#
# WHY: macOS launchd hands every process a soft RLIMIT_NOFILE of 256
# (`launchctl limit maxfiles`). Fish opens fds for its universal-variable
# notifier plus every pipe, command substitution, and background job, so a
# bursty script can exhaust 256 and fail with "too many open files".
# The hard limit is unlimited, so raising the soft limit needs no privileges.
ulimit -Sn 65536
