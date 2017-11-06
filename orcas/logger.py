import sys

# TODO: detect os and replace \n with \r\n if was windows.
new_line_char = "\n"


def change_stdout(stream=None):
    sys.stdout = stream


def info(string_input, newline=True, prefix=True):
    sys.stdout.write("{}{}{}".format("[INFO] " if prefix else "", string_input, new_line_char if newline else ""))


def warn(string_input, newline=True):
    sys.stdout.write("[WARN] {}{}".format(string_input, new_line_char if newline else ""))


def error(string_input, newline=True):
    sys.stderr.write("[ERROR] {}{}".format(string_input, new_line_char if newline else ""))
