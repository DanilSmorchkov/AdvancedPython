import asyncio
import os
import uuid
from functools import partial

import aiohttp
import click


def save_image_sync(filename: str, data: bytes) -> None:
    """Save file synchronously"""
    with open(filename, "wb") as f:
        f.write(data)


async def download_image(
    session: aiohttp.ClientSession,
    output_dir: str,
    semaphore: asyncio.Semaphore,
    image_size: tuple[int, int] = (600, 600),
) -> None:
    """Download and save a single image asynchronously"""
    async with semaphore:
        url = f"https://picsum.photos/{image_size[0]}/{image_size[1]}"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    filename = os.path.join(output_dir, f"{uuid.uuid4()}.jpg")
                    loop = asyncio.get_running_loop()
                    await loop.run_in_executor(
                        None, partial(save_image_sync, filename, data)
                    )
                else:
                    click.echo(f"Download error: HTTP {response.status}")
        except Exception as e:
            click.echo(f"Image download failed: {str(e)}")


async def async_main(count: int, output_dir: str, image_size: tuple[int, int]) -> None:
    """Main async entry point"""
    os.makedirs(output_dir, exist_ok=True)
    semaphore = asyncio.Semaphore(20)

    client_timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        tasks = [download_image(session, output_dir, semaphore, image_size) for _ in range(count)]
        await asyncio.gather(*tasks)


@click.command()
@click.option(
    "-c", "--count", type=int, required=True, help="Number of images to download"
)
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=False, dir_okay=True),
    required=True,
    help="Output directory for images",
)
@click.option(
    "--size",
    type=(int, int),
    default=(600, 600),
    help="Image dimensions as WIDTH HEIGHT",
)
def main(count: int, output: str, size: tuple[int, int]) -> None:
    """
    Async image downloader for picsum.photos
    Downloads random images with specified parameters
    """
    click.echo(f"Starting download of {count} images to {output}")
    asyncio.run(async_main(count, output, size))
    click.echo("Download completed!")


if __name__ == "__main__":
    main()
