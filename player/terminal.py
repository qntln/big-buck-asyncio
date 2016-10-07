
# Move cursor to required position in terminal
MOVE_CURSOR_FORMAT = b'\033[%d;%dH'

# Reset cursor to 0,0
RESET_CURSOR = MOVE_CURSOR_FORMAT % (0, 0)

# Clear all lines in terminal
CLEAR = b'\x1b[2J'
