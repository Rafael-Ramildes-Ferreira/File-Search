# How testing ware conducted
The outpu ware compared with output of existing programs. I got the expected output with:

```find . -name "*cpython*" > test/find_output.txt```

And compared with the python program output got by:

```python FileSearch.py > test/python_output.txt```

Weirdly python's output has more lines, but it has no repeted line, as can be seen by running:

```sort test/python_output.txt | uniq -d > test/python_output_repeated_lines.txt```

by typing `ctrl + f` in the file, vscode find as many instances of the searched pattern than there is lines in the file.
Also, no error is returned from the following line:

```while read -r line; do   ls -l "$line"; done < test/python_output.txt```

This means that:

1. Every detected instance of the pattern is a different instance;

2. Every detected instance contains the searched pattern; and

3. Every detected instance is a real file or directory