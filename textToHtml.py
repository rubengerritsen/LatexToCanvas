#!/usr/bin/env python3

import sys
import subprocess
import shutil

options = {
    ######## USER INPUT #########
    "sectionNr": True,
    "TOC": True,
    "TOC_depth": 2,
    "pathToBib": "lib2.bib",
    "template": "canvasTemplate.html",
    "filters": ["highlightCode.py",
                "addEquationNumbers.py"]
    #############################
}


def helpMessage():
    return ("""
  OVERVIEW:
  This tool helps to convert LaTeX (.tex) of Markdown (.md) files to 
  plain HTML. It supports syntax highlighting for code blocks (lstlisting),
  equation numbers and links to equations. It provides these 
  functions in plain HTML, so no CSS or external sources are needed.
  The only thing it can't handle are images, it will process them,
  but they will probably not display in your HTML. They can however
  be added manually (not by this tool).

  DEPENDENCIES:
  This tool requires a working (and added to the path) installation 
  of pandoc:

    https://pandoc.org/installing.html

  To use the filters for syntax highlighting and equation numbering
  we need to have the following python packages installed (the 
  install command is a suggestion, conda, for example, comes with 
  these packages pre installed, they may be old though!).

  * pandocfilters (INSTALL: pip3 install pandocfilters)
  * pygments      (INSTALL: pip3 install pygments)

  USAGE:
  To use the tool simply run this file with as input parameter the
  .tex file and optionally the name of the output file. On Linux
  
    ./textToHtml.py <input>.tex
  
  or
  
    ./textToHtml.py <input>.tex <output>.html

  NB: for all the features to work the following files should be 
  accessible (preferably in the working directory) and .py files
  should be executable:

  * highlightCode.py
  * addEquationNumbers.py
  * htmlTemplate.html

  ADDITIONAL OPTIONS:
  To control the eventual look of the output HTML we can change
  all the default options in the textToHtml.py file, the options
  are at the top labelled 'USER INPUT'. The options to change

  * table of contents
  * section numbering
  * templates controls the layout of the HTML file
  * the bibliography source file
  * and which filters to use

  To change the colorscheme for syntax highlighting, change
  the style variable in the highlightCode.py filter source file.
  """)


def runPandoc(inputFile, outputFile="output.html", markdown=False):
    global options

    #defaults
    args = ["pandoc", "--mathml", "--standalone", "--to=html"]

    # input file format
    if markdown:
        args.append("--from=markdown")
    else:
        args.append("--from=latex")


    # Processing options
    if options["sectionNr"]:
        args.append("--number-offset=0")
    if options["TOC"]:
        args.append("--toc")
        if "TOC_depth" in options:
            args.append(f"--toc-depth={options['TOC_depth']}")
    if "pathToBib" in options:
        args.append(f"--bibliography={options['pathToBib']}")
    if "template" in options:
        args.append(f"--template={options['template']}")
    for filter in options["filters"]:
        args.append(f"--filter={filter}")

    args.append(f"--output={outputFile}")
    args.append(inputFile)
    # run pandocs
    print(f"Processing: {inputFile}")
    subprocess.Popen(args)
    print(f"HTML is written to: {outputFile}")


if __name__ == "__main__":
    if (shutil.which("pandoc") == None):
        print("No pandoc installation found.")
        exit()

    userOptions = sys.argv

    if len(userOptions) == 1:
        print("Please specify at least an input file (.tex or .md)")
        print("General usage: textToHtml.py <input>.tex <output>.html")
        print("For a help message use: textToHtml.py help")

    if len(userOptions) == 2:
        if userOptions[1][-4:] == ".tex":
            runPandoc(userOptions[1])
        elif userOptions[1][-3:] == ".md":
            runPandoc(userOptions[1], markdown=True)
        elif userOptions[1].find("help") != -1:
            print(helpMessage())
        else:
            print("Only .tex or .md files are supported.")

    if len(userOptions) == 3:
        if userOptions[1][-4:] == ".tex":
            runPandoc(userOptions[1], userOptions[2])
        elif userOptions[1][-3:] == ".md":
            runPandoc(userOptions[1], userOptions[2], markdown=True)
        else:
            print("Only .tex or .md files are supported.")
