#!/usr/bin/python3
## 2022-04-25
## Lukas Schönmann
## lukas.schoenmann@students.boku.ac.at
## PDF-Merger using Latex, runs in Linux terminal

__version__ = "0.1.0"

if __name__ == '__main__':

    import os
    import sys
    import argparse


    #-----Main-----#

    parser = argparse.ArgumentParser(description='Merge several PDF files into one file. Allows page selection and various layout parameters, including multiple pages per sheet. \nREQUIRES Latex!', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', help='Input files', type=str, nargs='+', required=True)
    parser.add_argument('-p', '--pages', help='Selected pages and layout modification for each file; default is all pages for every file \n   any number of pages can be selected, separated by commas "," \n   "-" selects all pages, or a range; can also be open \n   "_" creates a blank page \nprecede with optional layout parameters:\n   "L" for landscape orientation\n   "F" to fit the paper size\n   "N" to avoid automatic scaling', type=str, nargs='*', required=False, default="default")
    parser.add_argument('-a', '--path', help='Path to input directory; default is current directory "./"', type=str, default="./", required=False)
    parser.add_argument('-n', '--nup', help='Dimensions of the number of pages per sheet; pass for each file in delimited format using ","', type=str, nargs='?', required=False, default="1x1")
    parser.add_argument('-b', '--build', help='Build the latex file; default is true', required=False, action='store_false')
    parser.add_argument('-c', '--clean', help='Remove all Latex files created after building; default is true', required=False, action='store_false')
    parser.add_argument('-o', '--output', help='Output file name (including filename extension); default is "pdf-merger.pdf"', type=str, nargs='?', required=False, default="pdf-merger.pdf")
    parser.add_argument('-t', '--texname', help='Name of the latex .tex file (excluding filename extension); default is "pdf-merger.tex"', type=str, nargs='?', required=False, default="pdf-merger")
    args = parser.parse_args()

    #-----Preambel-----#

    texname = args.texname

    f = open(texname+".tex", "w")
    preambel = r"""\documentclass[11pt,a4paper]{article}
\usepackage{pdfpages} %%to insert whole pdf pages
\pagenumbering{gobble} %%remove page number
\begin{document}
%% Include all pdf's or images to be merged below 
%%'pages' for page selection (numbers; '-' for all and '{}' for empty pages)
%%'landscape=bool' for rotation
%%'nup=dimxdim' for multiple pages per sheet
%%'fitpaper=bool' to paper size to that of the insert (default is false)
%%'noautoscale=bool' to suppress scaling (default is false)

"""

    f.write(preambel)
    f.close()

    # read input arguments
    input_path = args.path
    nups = args.nup


    # if nups param is default, set to 1x1 for every file
    if nups == "1x1":
        i = 0
        while i < len(args.input):
            nups += ",1x1"
            i += 1
    nup_list = [item for item in nups.split(',')]



    #-----Main Body of File-----#

    # create main body of .tex file
    f = open(texname+".tex", "a")
    for file in args.input:

        # read page parameters for current file
        # or use "-" if default
        if args.pages == "default":
            pages = "-"
        else:
            pages = args.pages[args.input.index(file)]  
        # replace underscores with curly braces to allow for empty pages     
        pages = pages.replace("_", "{}")

        # list with all valid layout parameter characters
        paramlist = ["L", "F", "N"]

        # set .tex params according to arguments
        # NB: pages includes both page selection and layout modification
        params = ""
        if "L" in pages:
            params += ",landscape=true"
        if "F" in pages: 
            params += ",fitpaper=true"
        if "N" in pages:
            params += ",noautoscale=true"

        # if nup parameter is not default (1x1), set nup parameter
        if not nup_list[args.input.index(file)] == "1x1": 
            params += ",nup=" + nup_list[args.input.index(file)]

        # remove characters from paramlist from pages to allow passing as page selection
        for param in paramlist:
            if param in pages:
                pages = pages.replace(param, "")

        # write to .tex file
        f.write(r"\includepdf[pages={{{0}}}{2}]{{{3}{1}}}".format(pages, file, params, input_path) + "\n")
    f.close()

    #-----End of Document-----#

    f = open(texname+".tex", "a")
    f.write("\n\n"r"\end{document}")
    f.close()


    #-----Build and Cleanup-----#

    import subprocess

    if args.build:
        output = args.output
        # build .tex file
        process = subprocess.Popen(["pdflatex", texname+".tex"])
        process.wait()
        # create output directory
        os.makedirs("pdfmerger-output", exist_ok=True)
        # move to output directory and overwrite if necessary
        os.replace(texname+".pdf", os.path.join("pdfmerger-output", output))

    if args.clean:
        # remove all files created during build
        os.remove(texname+".tex")
        os.remove(texname+".log")
        os.remove(texname+".aux")
        os.remove(texname+".out")
        os.remove(texname+".fls")
        print("Cleaned up. Files removed: .tex, .log, .aux, .out, .fls")
  