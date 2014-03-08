from __future__ import absolute_import

import re
import sys

from ansicolor.ansicolor import Colors
from ansicolor.ansicolor import colorize
from ansicolor.ansicolor import colordiff
from ansicolor.ansicolor import get_highlighter
from ansicolor.ansicolor import highlight_string
from ansicolor.ansicolor import write_out


def demo_color():
    width = 10

    lst = []

    lst.extend([[], ['>>> Without colors'], []])
    line = []
    line.append(colorize("Standard".ljust(width), None))
    line.append(colorize("Bold".ljust(width), None, bold=True))
    line.append(colorize("Reverse".ljust(width), None, reverse=True))
    line.append(colorize("Bold & Rev".ljust(width), None, bold=True, reverse=True))  # noqa
    lst.append(line)

    lst.extend([[], ['>>> Using colors'], []])
    for color in Colors.iter():
        line = []
        line.append(colorize(color.__name__.ljust(width), color))
        line.append(colorize(color.__name__.ljust(width), color, bold=True))  # noqa
        line.append(colorize(color.__name__.ljust(width), color, reverse=True))  # noqa
        line.append(colorize(color.__name__.ljust(width), color, bold=True, reverse=True))  # noqa
        lst.append(line)

    lst.extend([[], ['>>> Using highlighting colors'], []])
    for color in Colors.iter():
        color = get_highlighter(color.id)
        line = []
        line.append(colorize(color.__name__.ljust(width), color))
        line.append(colorize(color.__name__.ljust(width), color, bold=True))  # noqa
        line.append(colorize(color.__name__.ljust(width), color, reverse=True))  # noqa
        line.append(colorize(color.__name__.ljust(width), color, bold=True, reverse=True))  # noqa
        lst.append(line)

    for line in lst:
        for item in line:
            write_out('%s  ' % item)
        write_out("\n")

def demo_highlight():
    rxs = [
        '(b+).*\\1',
        '(c+).*\\1',
        '(d+).*\\1',
        '(e+).*\\1',
    ]
    s = """\
aaabbbcccdddeeefffeeedddcccbbbaaa
fffeeedddcccbbbaaabbbcccdddeeefff
"""
    def display(rxs, s):
        spanlists = []
        for rx in rxs:
            spanlist = []
            for m in re.finditer(rx, s):
                spanlist.append(m.span())
            spanlists.append(spanlist)
        s = highlight_string(s, *spanlists)
        for (i, rx) in enumerate(rxs):
            color = get_highlighter(i)
            color = colorize(color.__name__.ljust(10), color)
            write_out('Regex %s: %s %s\n' % (i, color, rx))
        write_out(s)

    for i in range(0, len(rxs) + 1):
        write_out('\n')
        display(rxs[:i], s)

def demo_diff():
    def display_diff(s, t):
        (s_fmt, t_fmt) = colordiff(s, t)
        write_out('>>> %s\n' % s_fmt)
        write_out('    %s\n\n' % t_fmt)

    display_diff('first last', 'First Last')
    display_diff('the the boss', 'the boss')
    display_diff('the coder', 'the first coder')
    display_diff('agcat', 'gac')
    display_diff('XMJYAUZ', 'MZJAWXU')
    display_diff('abcdfghjqz', 'abcdefgijkrxyz')


if __name__ == '__main__':
    try:
        action = sys.argv[1]
    except IndexError:
        print("Usage:  %s [ --color | --highlight | --diff ]" % sys.argv[0])
        sys.exit(1)

    if action == '--color':
        demo_color()
    elif action == '--highlight':
        demo_highlight()
    elif action == '--diff':
        demo_diff()
