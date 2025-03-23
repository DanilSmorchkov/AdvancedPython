import click
import sys


@click.command()
@click.argument("files", nargs=-1, type=click.Path())
def wc(files):
    """Count lines, words, and bytes in the given files or from standard input."""
    if not files:
        data = sys.stdin.buffer.read()
        lines = data.count(b"\n")
        words = len(data.split())
        bytes_count = len(data)
        click.echo(f"{lines:7} {words:7} {bytes_count:7}")
    else:
        total_lines = 0
        total_words = 0
        total_bytes = 0

        for filename in files:
            try:
                with open(filename, "rb") as f:
                    data = f.read()
            except FileNotFoundError as e:
                click.echo(
                    f"wc: Cannot open '{filename}' for reading: {e.strerror}", err=True
                )
                continue

            lines = data.count(b"\n")
            words = len(data.split())
            bytes_count = len(data)
            total_lines += lines
            total_words += words
            total_bytes += bytes_count

            click.echo(f"{lines:7} {words:7} {bytes_count:7} {filename}")

        if len(files) > 1:
            click.echo(f"{total_lines:7} {total_words:7} {total_bytes:7} total")


if __name__ == "__main__":
    wc()
