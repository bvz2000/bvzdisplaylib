"""
A library to display things on screen.
"""

from __future__ import print_function

import math
import sys

# define some colors
# ----------------------------------------------------------------------------------------------------------------------
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'
ENDC = '\033[0m'
BG_RED = "\u001b[41m"
BLINK = "\033[5m"


# ----------------------------------------------------------------------------------------------------------------------
def display_progress(count,
                     total,
                     old_percent,
                     width=50,
                     completed_char="#",
                     empty_char=".",
                     postpend_str=""):
    """
    Draws and updates ASCII progress bar on the stdout.

    :param count:
           The current count for our progress bar.
    :param total:
           The count at 100%.
    :param old_percent:
           The previous percent. Necessary to prevent updates if the percentage has not changed since the last call.
    :param width:
           How wide to draw the progress bar in characters. If given an odd number, it will be rounded down to the
           nearest even value.
    :param completed_char:
           The character to display for a completed chunk.
    :param empty_char:
           The character to display for an as-yet uncompleted chunk.
    :param postpend_str:
           An arbitrary (and optional) string to append to the end of the progress bar.

    :return: The percent value for the current state.
    """

    # only allow even numbered widths
    if width % 2 != 0:
        width -= 1

    # calculate the percent
    percent = round((count * 1.0) / total * 100, 1)

    # only update the display if the percentage has changed
    if percent == old_percent and percent != 0:
        return percent

    # build the completed and uncompleted portions of the progress bar
    done_str = "{0}".format(completed_char * (int(round(percent / (100 / width), 0))))
    empty_str = "{0}".format(empty_char * (width - (int(round(percent / (100 / width))))))

    # build the X out of Y text
    count_str = " (" + BRIGHT_WHITE + str(count) + ENDC + " of " + BRIGHT_WHITE + str(total) + ENDC + ")"

    # build the percent string
    percent_str = "{0}".format(" " * (4 - len(str(int(math.floor(percent)))))) + str(percent) + "%" + " "

    # build the complete string, and insert the percent
    progress_bar_str = "[" + done_str + empty_str + "]"
    progress_left = progress_bar_str[:int((len(progress_bar_str) / 2) - math.floor(len(percent_str) / 2)) + 2]
    progress_right = progress_bar_str[int((len(progress_bar_str) / 2) + math.ceil(len(percent_str) / 2)) + 2:]
    progress_bar_str = progress_left
    progress_bar_str += BRIGHT_YELLOW + percent_str + ENDC
    progress_bar_str += progress_right

    # append the count string
    progress_bar_str += count_str

    # append the postpend string
    progress_bar_str += postpend_str

    # show it
    sys.stdout.write(progress_bar_str)
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(progress_bar_str)))  # return to start of line

    # return the percent (so that we only update the percentage when it changes)
    return percent


# ----------------------------------------------------------------------------------------------------------------------
def display_error(*msgs):
    """
    Given any number of args, converts those args to strings, concatenates them, and prints to stdErr.

    :return: Nothing.
    """

    output = ""
    for msg in msgs:
        output += " " + str(msg)
    print(output.lstrip(" "), file=sys.stderr)


# ----------------------------------------------------------------------------------------------------------------------
def format_string(msg):
    """
    Given a string (msg) this will format it with colors based on the {{COLOR}} tags. (example {{COLOR_RED}}). It will
    also convert literal \n character string into a proper newline.

    :param msg:
           The string to format.

    :return: The formatted string.
    """

    output = msg.replace(r"\n", "\n")
    output = output.replace("{{", "{")
    output = output.replace("}}", "}")

    try:
        output = output.format(
            BLACK=BLACK,
            RED=RED,
            GREEN=GREEN,
            YELLOW=YELLOW,
            BLUE=BLUE,
            MAGENTA=MAGENTA,
            CYAN=CYAN,
            WHITE=WHITE,
            BRIGHT_RED=BRIGHT_RED,
            BRIGHT_GREEN=BRIGHT_GREEN,
            BRIGHT_YELLOW=BRIGHT_YELLOW,
            BRIGHT_BLUE=BRIGHT_BLUE,
            BRIGHT_MAGENTA=BRIGHT_MAGENTA,
            BRIGHT_CYAN=BRIGHT_CYAN,
            BRIGHT_WHITE=BRIGHT_WHITE,
            COLOR_NONE=ENDC,
            BG_RED=BG_RED,
            BLINK=BLINK,
        )
    except KeyError:
        pass

    output += ENDC

    return output


# ----------------------------------------------------------------------------------------------------------------------
def display_message(*msgs: object):
    """
    Given any number of args, converts those args to strings, concatenates them, and prints to stdOut.

    :return: Nothing.
    """

    msg = " ".join([str(item) for item in msgs])
    msg = format_string(msg)
    print(msg)


# ----------------------------------------------------------------------------------------------------------------------
def multiple_choice_user_input(*msgs,
                               legal_answers,
                               alternate_legal_answers=None,
                               default=None,
                               blank_lines=0):
    """
    Get a user input.

    :param msgs:
           The prompt to display to the user. This may be a series of strings.
    :param legal_answers:
           A list of legal answers to the prompt. These will be presented in all upper case to the user. Note, the legal
           answers must include some sort of quit option since this function will keep looping until a legal answer is
           received.
    :param alternate_legal_answers:
           An optional dictionary of alternate legal answers that will be accepted, but not displayed to the user.
           The key is the alternate legal answer and the value is the actual legal answer that this alternate maps tp.
           Primarily used to provide alternates that the user might type in but are not necessary to display. Example:
           the user may be presented with the legal answers "YES" and "NO", but additional accepted values may be "Y"
           and "N". In this case, alternate_legal_answers would be {"Y": "YES", "N": "NO"}
    :param default:
           Which of the legal answers is the default answer. If None, there is no default. Defaults to None.
    :param blank_lines:
           How many blank lines to display before the first instance of the prompt. Defaults to 0.

    :return: The legal answer that was returned.
    """

    assert type(legal_answers) is list
    assert alternate_legal_answers is None or type(alternate_legal_answers) is dict
    assert default is None or type(default) is str
    assert type(blank_lines) is int

    options = [item.upper() for item in legal_answers]

    if alternate_legal_answers is not None:
        for key, value in alternate_legal_answers.items():
            assert value.upper() in options

    if default is not None:
        assert default.upper() in options

    alternate_options = list()
    if alternate_legal_answers is not None:
        alternate_options = [item.upper() for item in alternate_legal_answers.keys()]

    alternate_legal_answers_upper = dict()
    if alternate_legal_answers is not None:
        for key in alternate_legal_answers.keys():
            alternate_legal_answers_upper[key.upper()] = alternate_legal_answers[key]

    options_str = f"({','.join(options)})"

    if blank_lines > 0:
        display_message("\n" * blank_lines)

    result = ""
    while result.upper() not in legal_answers and result.upper() not in alternate_options:
        display_message(*msgs, options_str)

        if default is None:
            prompt = "> "
        else:
            prompt = format_string(f"({{BRIGHT_YELLOW}}{default.upper()}{{COLOR_NONE}}) > ")

        try:
            result = input(prompt)
        except KeyboardInterrupt:
            sys.exit()

        if result == "" and default is not None:
            result = default.upper()

    if result.upper() in alternate_options:
        result = alternate_legal_answers_upper[result.upper()]

    return result.upper()


# ----------------------------------------------------------------------------------------------------------------------
def format_boolean(value,
                   colorize=True,
                   invert_color=False):
    """
    Converts a boolean value into a Yes or No. If colorize is True, then Yes will be returned as green, and no will be
    returned as red.

    :param value:
           A boolean either passed as a boolean or as a string.
    :param colorize:
           If True, then the returned string will be formatted green for True, or red for False. Defaults to True.
    :param invert_color:
           If True (and if colorize) is True, then True will be red, and False will be green. Defaults to False.


    :return: A string containing either "Yes" or "No" depending on the original boolean value.
    """

    assert type(value) is bool or (type(value) is str and value.upper() in ("TRUE", "FALSE"))

    if str(value).upper() == "TRUE":
        color = "BRIGHT_GREEN"
        return_value = "Yes"
    else:
        color = "BRIGHT_RED"
        return_value = "No"

    if colorize:
        return_value = format_string("{{" + color + "}}" + return_value)

    return return_value


# ----------------------------------------------------------------------------------------------------------------------
def display_refreshable_message(*msgs):
    """
    Given any number of args, converts those args to strings, concatenates them, and prints to stdOut. Then resets the
    output to be back at the beginning f the line ready for the next string to overwrite the just printed string. NOTE:
    THIS ONLY WORKS FOR STRINGS THAT STAY THE SAME LENGTH OR GROW IN LENGTH. If the string shrinks in length, part of
    the previous message will be left behind. To counter this (if you have potentially shrinking strings), it may be
    necessary to pad your strings with spaces at the end to a known length.

    :return: Nothing.
    """

    # Print the message, flush buffer, and move back to the beginning of the line.
    message = " ".join([str(item) for item in msgs])
    message = format_string(message)
    sys.stdout.write(message)
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(message)))


# ----------------------------------------------------------------------------------------------------------------------
def flush_refreshable_message(length=80):
    """
    Call to clear out the current line. Used primarily when a line has been half printed and needs to be removed. This
    does NOT move the cursor to a new line, it just clears out the current line and leaves the cursor at the beginning.

    :param length: How many spaces to flush. Defaults to 80.

    :return: Nothing.
    """

    sys.stdout.write("\b" * length)
    sys.stdout.write(" " * length)
    sys.stdout.write("\b" * length)
    sys.stdout.flush()


# ----------------------------------------------------------------------------------------------------------------------
def finish_refreshable_message():
    """
    Called when the refreshable message is no longer needed (prevents the next printed statement from overwriting the
    last version of the refreshed message).

    :return: Nothing.
    """

    print()
