import click
import sys


@click.command()
@click.argument("filename", required=False, type=click.Path())
@click.option(
    "-b",
    "--body-numbering",
    default="a",
    type=click.Choice(["a", "t", "n"]),
    help="Numbering style: a=all, t=non-empty, n=none (default: a)",
)
def number_lines(filename, body_numbering):
    """Number lines from a file/stdin like 'nl -b a' with style support."""
    try:
        if filename:
            with open(filename, "r") as f:
                lines = f.readlines()
        else:
            lines = click.get_text_stream("stdin").readlines()

        counter = 1
        for line in lines:
            cleaned_line = line.rstrip("\n")

            if body_numbering == "a":
                click.echo(f"{counter:6}\t{cleaned_line}")
                counter += 1
            elif body_numbering == "t":
                if cleaned_line.strip():
                    click.echo(f"{counter:6}\t{cleaned_line}")
                    counter += 1
                else:
                    click.echo(f"{'':6}\t{cleaned_line}")
            elif body_numbering == "n":
                click.echo(f"{'':6}\t{cleaned_line}")

    except OSError as e:
        click.echo(
            f"nl: Cannot open '{filename}' for reading: {e.strerror}",
            err=True,
        )
        sys.exit(1)


if __name__ == "__main__":
    number_lines()
