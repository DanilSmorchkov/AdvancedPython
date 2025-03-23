import click
import sys


@click.command()
@click.argument("files", nargs=-1, type=click.Path())
def tail(files):
    """Prints the last 10 lines of each file or 17 lines from stdin if no files are provided."""
    if not files:
        lines = sys.stdin.readlines()
        count = 17
        output = lines[-count:] if len(lines) >= count else lines
        click.echo("".join(output), nl=False)
    else:
        for idx, filename in enumerate(files):
            if len(files) > 1:
                click.echo(f"==> {filename} <==")
            try:
                with open(filename, "r") as f:
                    lines = f.readlines()
                    count = 10
                    output = lines[-count:] if len(lines) >= count else lines
                    click.echo("".join(output), nl=False)
            except OSError as e:
                click.echo(
                    f"tail: Cannot open '{filename}' for reading: {e.strerror}",
                    err=True,
                )
                continue


if __name__ == "__main__":
    tail()
