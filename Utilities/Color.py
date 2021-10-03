import sys
import os
# FILE SOURCE CODE : https://github.com/diogo-fernan
#
#
# TODO: VALIDATE THIS.
#  #
#  SOURCE: https://en.wikipedia.org/wiki/ANSI_escape_code
#  decoy =  "\x1b[;92m mensagem\x1b[0m"
#   soh = "\x01"
#   sot = "\x02"
#   esc = "\x1b"
#                  ouutput of below function  "color" <-      \x01\x1b[x1b;{color}m'textoparaenviar'\x01\x1b[\x02m

class asciic:
    # SOURCE: INFO
    # SOURCE https://stackoverflow.com/questions/15011478/ansi-questions-x1b25h-and-x1be
    # These are ANSI escape sequences (also known as VT100 codes) are an early standardisation of
    # control codes pre-dating ASCII.
    #
    # The escape sequence \x1BE, or Esc+E, is NEL or "Next line",
    # and is used on older terminals and mainframes to denote CR+LF, or \r\n.
    #
    # The escape sequence \x1B[ (Esc+[) is an example of a Control Sequence Introducer.
    # (\x9B is another single-character CSI.) The control sequence ?25h following it is used to show the cursor.
    #
    # Most terminals will support these control codes;
    # to enter escape sequences you can type Ctrl+V,
    # Ctrl+[ which should render as ^[ (the C0 code for ESC),
    # followed by the escape code.

    # TRIVIA: https://en.wikipedia.org/wiki/ANSI_escape_code

    soh = "\x01"
    sot = "\x02"
    esc = "\x1b"


class code:
    """
    styles and bright foreground colors
    """
    end = 0
    bold = 1
    underline = 4

    gray = 90
    red = 91
    green = 92
    yellow = 93
    blue = 94
    magenta = 95
    cyan = 96
    black = 97


def color(string, color, bold=False, underline=False):
    if sys.platform == "win32" and os.getenv("TERM") != "xterm":
        return str(string)
    bu = ""
    if bold:
        bu = code.bold
    elif underline:
        bu = code.underline
    # return f"{asciic.soh+asciic.esc}" \
    # 	   f"[{bu};{c}m{asciic.sot}{s}{asciic.soh+asciic.esc}" \
    # 	   f"[{code.end}m{asciic.sot}"



    return f"{asciic.esc}" \
           f"[{bu};{color}m{string}{asciic.esc}" \
           f"[{code.end}m"



def bold(string):
    return color(string, code.bold)


def gray(string):
    return color(string, code.gray)


def grayb(string):
    return color(string, code.gray, bold=True)


def grayu(string):
    return color(string, code.gray, underline=True)


def red(string):
    return color(string, code.red)


def redb(string):
    return color(string, code.red, bold=True)


def redu(string):
    return color(string, code.red, underline=True)


def green(string):
    return color(string, code.green)


def greenb(string):
    return color(string, code.green, bold=True)


def greenu(string):
    return color(string, code.green, underline=True)


def yellow(string):
    return color(string, code.yellow)


def yellowb(string):
    return color(string, code.yellow, bold=True)


def yellowu(string):
    return color(string, code.yellow, underline=True)


def blue(string):
    return color(string, code.blue)


def blueb(string):
    return color(string, code.blue, bold=True)


def blueu(string):
    return color(string, code.blue, underline=True)


def magenta(string):
    return color(string, code.magenta)


def magentab(string):
    return color(string, code.magenta, bold=True)


def magentau(string):
    return color(string, code.magenta, underline=True)


def cyan(string):
    return color(string, code.cyan)


def cyanb(string):
    return color(string, code.cyan, bold=True)


def cyanu(string):
    return color(string, code.cyan, underline=True)


def black(string):
    return color(string, code.black)


def blackb(string):
    return color(string, code.black, bold=True)


def blacku(string):
    return color(string, code.black, underline=True)

def test_color():
    """
    Put some color lines to stdout
    """

    lines = ['\tAlthough never is often better than *right* now.',
            '\tIf the implementation is hard to explain, it"s a bad idea.',
            '\tIf the implementation is easy to explain, it may be a good idea.']

    print(bold(lines[0]))
    print(bold(lines[1]))
    print(bold(lines[2]))
    print(green(lines[0]))
    print(green(lines[1]))
    print(green(lines[2]))
    print(red(lines[0]))
    print(red(lines[1]))
    print(red(lines[2]))
    print(gray(lines[0]))
    print(gray(lines[1]))
    print(gray(lines[2]))
    print(blue(lines[0]))
    print(blue(lines[1]))
    print(blue(lines[2]))
    print(yellow(lines[0]))
    print(yellow(lines[1]))
    print(yellow(lines[2]))
    print(magenta(lines[0]))
    print(magenta(lines[1]))
    print(magenta(lines[2]))
    print(cyan(lines[0]))
    print(cyan(lines[1]))
    print(cyan(lines[2]))
    print(black(lines[0]))
    print(black(lines[1]))
    print(black(lines[2]))