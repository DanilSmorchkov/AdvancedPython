import click
import sys


@click.command()
@click.argument("files", nargs=-1, type=click.Path())
def wc(files):
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
        stats = []
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
            stats.append((lines, words, bytes_count, filename))
            total_lines += lines
            total_words += words
            total_bytes += bytes_count
        for entry in stats:
            click.echo(f"{entry[0]:7} {entry[1]:7} {entry[2]:7} {entry[3]}")
        if len(files) > 1:
            click.echo(f"{total_lines:7} {total_words:7} {total_bytes:7} total")


if __name__ == "__main__":
    wc()
