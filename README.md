csv2table is a simple tool that reads comma-separated values from stdin and returns valid [LaTeX](https://www.latex-project.org/) tabular syntax to stdout. This is far from the first tool that attempts to tackle LaTeX tables, but it differs from its comrades in some regards. Rather than operating on external files with an extended suite of rendering options, csv2table writes tables interactively, accepting piped selections directly from an editor such as vim, and returning its output back to the session itself:

[![table rendered in LaTeX](https://raw.githubusercontent.com/jimd1989/csv2table/master/csv2latex-2.gif)](https://raw.githubusercontent.com/jimd1989/csv2table/master/csv2latex-2.gif)

This allows users to quickly compose skeletal table outlines, which can then be fine-tuned in the editor. You may find this preferable to juggling a million flags. 

## Requirements

[Python 3](https://www.python.org/)

## Installation

+ `make`
+ `make install` (may have to be root)
+ `make uninstall` (to remove)

## Usage

Running csv2table outside of a pipe will drop the user into an input loop. This isn't very useful unless the output is redirected, since the stdin/stdout text will be intermingled. Usually you'll want to pipe input to the program.

csv2table has some command-line flags:

+ `-h`: Display the help message.
+ `-a`: Create a full stand-alone LaTeX document to accompany the table.
+ `-b`: Use the "booktabs" package to draw horizontal rules.
+ `-box`: Draw a box around the table.
+ `-c`: Center-align all table elements.
+ `-d`: Set a different delimiter to replace the comma. For tabs, please use c^v <tab> rather than '\t`'.
+ `-f`: Set font size of stand-alone LaTeX document. 'pt' is not required: just the number.
+ `-grid`: Draw a grid around the table elements.
+ `-i`: The number of spaces to index LaTeX code rows. Has no effect on the placement of elements in the final rendered document.
+ `l`: Left-align all table elements (default behavior).
+ `r`: Right-align all table elements.
+ `s`: Set the stretch factor (padding) of table elements. Should be a float value.
+ `t`: Provide a custom table layout string, such as '|l| r c', for more advanced rendering. This option requires the user to know the exact number of columns.

csv2table also accepts other forms of input:

+ `#`: Comment text. Is ignored.
+ `!`: Literal text. Is echoed and not treated like a table row.
+ `---`: A top or bottom horizontal rule.
+ `--`: A middle horizontal rule.

## Example

    # This will be ignored. Don't worry.
    ---
    this,is,an
    --
    example,of,a
    csv,to,table
    ---

This file is run through:

    cat example-input | csv2table -a -b -c -f 12 -s 2.5 > table.tex

And compiles to:

    \documentclass[a4paper,12pt]{article}
    \usepackage{booktabs}
    \begin{document}
    \pagenumbering{gobble}
    \bgroup
    \def\arraystretch{2.5}%
    \begin{tabular}{c c c} 
        \toprule
         this & is & an \\
    \midrule
         example & of & a \\
         csv & to & table \\
    \bottomrule
    \end{tabular}
    \egroup
    \end{document}

And looks like:

[![table rendered in LaTeX](https://raw.githubusercontent.com/jimd1989/csv2table/master/csv2latex-1.png)](https://raw.githubusercontent.com/jimd1989/csv2table/master/csv2latex-1.png)

Play with the options until you get something you like. You can always edit the LaTeX code itself of course.
