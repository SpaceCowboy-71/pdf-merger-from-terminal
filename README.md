# pdf-merger-from-terminal
An easy-to-use PDF file merger running in the terminal, combining multiple input files into one. Allows page selection and various layout parameters, including multiple pages per sheet. Also accepts `.png` for input files. 
What it does is that the tool creates an intermediate `.tex` file containing commands from the `pdfpages` file, along with the parameters specified for each input file. This `.tex` file subsequently is being built using `pdflatex`. Intermediate and helper files are deleted afterwards, but this cleanup step can be suppressed. 

REQUIRES LaTeX and Python!

# Examples

The simplest way to use this tool is by only selecting input PDF files, using the `--input` or `-i` flag. The merger automatically includes all pages of every file without special layout modifications (i.e., it scales every input page to A4 paper size). Input files are taken from the current directory, but paths can be specified. Note that the order of the input files also determines their order in the merged file. Input files can be called multiple times. 

```
$ ./pdf-merger-from-terminal.py --input file-1.pdf file-2.pdf
```

The tool will create an output directory in the current directory called `pdfmerger-output`. Inside, you will find the merged file; its default name is `pdf-merger.pdf`. 

## Page Selection and Layout Modification

For each file, pages to be merged can be selected, and optional layout parameters can be set. Both works in one step by setting the `--pages` or `-p` flag. For each input file, page selection and layout modification must happen individually. Arguments are to be passed separated by a white space and in the order of the input files, without skipping a file. 

To select a range of pages, connect numbers with a dash `-`. Ranges can have open ends, thus allowing selection of ranges from the first page or to the last page. A dash without page numbers hence selects all pages of the input file. Single pages can be selected by specifying their number. Pages can be selected multiple times. To insert blank pages use the underscore `_`. All page selection parameters can be combined using commas `,`. By default, all pages are selected for each input file. 

Optional layout modifiers consist of single capital letters. Precede the page selection with any number of them. Do not use white spaces inbetween. The following modifiers are available:  
* `L` to switch to landscape orientation (`pdfpages`'s `landscape=true`)
* `F` to adjust the paper size to the one of the inserted document (`pdfpages`'s `fitpaper=true`)
* `N` to suppress automatic scaling of the document(`pdfpages`'s `noautoscale=true`)

As an example: 

```
$ ./pdf-merger-from-terminal.py --input file-1.pdf file-2.png file-3.pdf --pages 1,_ FN- L1,3-5
```
The merged file would contain the first page of file 1, then a blank page. All pages of file 2 (which is a `.png` but still needs page selection) would be included, but the paper size of the image would be fitted to the one of the input file and without automatically scaling it. For file 3, pages one, three, four and five would be included in landscape orientation. 

## Input and Output Management

By default, the path of the input files starts from the current directory. This can be changed by setting the `--path` or `-a` flag. For instance, the following two lines produce identical output: 

```
$ ./pdf-merger-from-terminal.py --input input/file-1.pdf input/file-2.pdf
$ ./pdf-merger-from-terminal.py --input file-1.pdf file-2.pdf --path input/
```

The file name of the merged output file can also be specified by setting the `--output` or `-o` flag. The full name has to be specified, including the filename extension. The default name is `pdf-merger.pdf`.   
Similarly, the filename of the latex intermediate files can be specified by setting the `--texname` or `-t` flag. No filename extension must be specified here. The default name is `pdf-merger`. Note that this option is mostly relevant if the user chooses to skip the cleanup step (`--noclean`), as all intermediate files are removed otherwise. 

## Pages per Sheet

The dimensions of the number of pages per sheet (columns times rows) can be specified by setting the `--nup` or `-n` flag. By default, one page is displayed per sheet (`1x1`). If the number of pages are manually set it must be for every input file in the same order and as one argument, separating the dimensions `<num>x<num>` with commas `,`. For instance: 

```
$ ./pdf-merger-from-terminal.py --input file-1.pdf file-2.pdf --nup 1x2,2x2
```
The resulting merged file would include all pages of file 1 with one column and two rows per page, and all pages of file 2 with two columns and rows per page. 

## Advanced Use

A user may be interested in creating a `.tex` file for further use, like incorporating it into an existing LaTeX document or to take a look at the code for debugging purposes. In this case, the cleanup step can be suppressed by adding the `--noclean` or `-c` flag. This results in the `.tex` file and all the LaTeX helper files like `.log`, `.aux` or `.out` to be kept in the same directory as the tool.  
Additionally, building the `.tex` file and thus creating the merged file might not be desired. In this case, the build step can be suppressed by adding the `--nobuild` or `-b` flag. Both flags need no arguments, passing them is enough. For instance: 

```
$ ./pdf-merger-from-terminal.py --input file-1.pdf file-2.pdf --nobuild --noclean
```
Take a look at the section __Input and Output Management__ to find out how to rename the resulting LaTeX files. 


