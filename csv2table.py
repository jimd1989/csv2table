#!/usr/local/bin/python3
from sys import stdin
import argparse

# Default values
alignment = 'l'
border = 'none'
stretch_factor = '1.0'
toprule = ''

# Default options
custom_header = False
standalone = False
stretch = False
booktabs = False

# Parsing command-line options
parser = argparse.ArgumentParser('<stdin> | csv2table')
parser.add_argument('-a', action='store_true', help='Create standalone tex document')
parser.add_argument('-b', action='store_true', help='Use booktab rules')
parser.add_argument('-box', action='store_true', help='Draw box border')
parser.add_argument('-c', action='store_true', help='Align all elements center')
parser.add_argument('-d', default=',', help='Table column delimiter')
parser.add_argument('-f', default='10', help='Font size in standalone document')
parser.add_argument('-grid', action='store_true', help='Draw grid border')
parser.add_argument('-i', type=int, default=4, help='Number of spaces to indent elements')
parser.add_argument('-l', action='store_true', help='Align all elements left')
parser.add_argument('-r', action='store_true', help='Align all elements right')
parser.add_argument('-s', default='1.0', help='Table stretch factor')
parser.add_argument('-t', default='nil', help='Custom table layout string')
args = parser.parse_args()
if args.a:
    standalone = True
if args.b:
    booktabs = True
if args.box:
    border = 'box'
if args.c:
    alignment = 'c'
delimiter = args.d
font = args.f
if args.grid:
    border = 'grid'
indent = ''.join([' '] * args.i)
if args.l:
    alignment = 'l'
if args.r:
    alignment = 'r'
if args.s != '1.0':
    stretch = True
    stretch_factor = args.s
if args.t != 'nil':
    custom_header = args.t

# Global reader state
first_line_read = False
previous_line_read = False

# Returning proper rule types
def rule(type):
    if booktabs:
        if type == 'top':
            return '\\toprule'
        if type == 'mid':
            return '\\midrule'
        if type == 'bottom':
            return '\\bottomrule'
    else:
        return '\\hline'

# Returning proper header string
def make_header(alignment, border, custom, xs):
    if custom:
        return custom
    fields_n = len(xs)
    fields = [alignment] * fields_n
    if border == 'box':
        return '| ' + ' '.join(fields) + ' |'
    if border == 'grid':
        return '| ' + ' | '.join(fields) + ' |'
    else:
        return ' '.join(fields)

# Placing standalone header
if standalone:
    print('\\documentclass[a4paper,{}pt]{{article}}'.format(font))
    if booktabs:
        print('\\usepackage{booktabs}')
    print('\\begin{document}')
    print('\\pagenumbering{gobble}')

# Main parser
for line in stdin:
    line = line.rstrip('\n')
    # ! Text is passed literally
    if line[0] == '!':
        print(line[1:])
    # # Text is commented out
    elif line[0] != '#' and not line.isspace():
        xs = line.split(delimiter)
        if not first_line_read:
            if line == '---':
                toprule = '\n' + indent + rule('top')
            else:
                header = make_header(alignment, border, custom_header, xs)
                if stretch:
                    print('\\bgroup')
                    print('\\def\\arraystretch{{{}}}%'.format(stretch_factor))
                print('\\begin{{tabular}}{{{}}}'.format(header), toprule)
                first_line_read = True
        if line == '---':
            if first_line_read:
                print(rule('bottom'))
        elif line == '--':
            print(rule('mid'))
        else:
            if previous_line_read and border == 'grid':
                print(rule('mid'))
            print(indent,' & '.join(xs), '\\\\')
            previous_line_read = True
print('\\end{tabular}')
if stretch:
    print('\\egroup')
if standalone:
    print('\\end{document}')
