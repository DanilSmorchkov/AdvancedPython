### nl:
```console
(AdvancedPython) ➜  homework_1 git:(hw1) ✗ uv run nl.py nl.py
     1  import click
     2  import sys
     3
     4
     5  @click.command()
     6  @click.argument("filename", required=False, type=click.Path())
     7  @click.option(
     8      "-b",
     9      "--body-numbering",
    10      default="a",
    11      type=click.Choice(["a", "t", "n"]),
    12      help="Numbering style: a=all, t=non-empty, n=none (default: a)",
    13  )
    14  def number_lines(filename, body_numbering):
    15      """Number lines from a file/stdin like 'nl -b a' with style support."""
    16      try:
    17          if filename:
    18              with open(filename, "r") as f:
    19                  lines = f.readlines()
    20          else:
    21              lines = click.get_text_stream("stdin").readlines()
    22
    23          counter = 1
    24          for line in lines:
    25              cleaned_line = line.rstrip("\n")
    26
    27              if body_numbering == "a":
    28                  click.echo(f"{counter:6}\t{cleaned_line}")
    29                  counter += 1
    30              elif body_numbering == "t":
    31                  if cleaned_line.strip():
    32                      click.echo(f"{counter:6}\t{cleaned_line}")
    33                      counter += 1
    34                  else:
    35                      click.echo(f"{'':6}\t{cleaned_line}")
    36              elif body_numbering == "n":
    37                  click.echo(f"{'':6}\t{cleaned_line}")
    38
    39      except OSError as e:
    40          click.echo(
    41              f"nl: Cannot open '{filename}' for reading: {e.strerror}",
    42              err=True,
    43          )
    44          sys.exit(1)
    45
    46
    47  if __name__ == "__main__":
    48      number_lines()
```

### tail:
```console
(AdvancedPython) ➜  homework_1 git:(hw1) ✗ uv run tail.py tail.py
                    click.echo("".join(output), nl=False)
            except OSError as e:
                click.echo(
                    f"tail: Cannot open '{filename}' for reading: {e.strerror}",
                    err=True,
                )


if __name__ == "__main__":
    tail()
```

### wc:
```console
(AdvancedPython) ➜  homework_1 git:(hw1) ✗ uv run wc.py wc.py tail.py nl.py
     44     114    1268 wc.py
     34     103    1041 tail.py
     48     108    1379 nl.py
    126     325    3688 total
```
