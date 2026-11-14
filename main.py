"""food-picture-01 entry: write the entry's food picture to the output dir.

The picture ships beside this program as ``entry.png`` (a JPEG file under a
.png name, which the gate allows: it tells PNG from JPEG by the first bytes).
The program simply copies those bytes to ``entry.png`` in the output
directory, so both grader runs write exactly the same file.

The output directory is ``$MAKEFUN_OUTPUT_DIR`` when set, else ``/output``.
The picture is looked for next to this program first, then in ``/bot`` (the
grader mounts the repository there), then in the working directory.
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576  # the gate's 1 MiB cap


def find_picture() -> str:
    """Return the path of the shipped entry.png, or raise FileNotFoundError."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "entry.png"),
        os.path.join("/bot", "entry.png"),
        os.path.join(os.getcwd(), "entry.png"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("entry.png not found beside the program")


def check_picture(path: str) -> None:
    """Guard the copy: the gate only takes a whole PNG or JPEG up to 1 MiB.

    The file is recognised by its first bytes, exactly as the gate does:
    PNG starts with 89 50 4E 47, JPEG with FF D8. Anything else, or a file
    over the cap, is refused here instead of being written to the output.
    """
    with open(path, "rb") as handle:
        head = handle.read(4)
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the 1 MiB cap")
    if not (head.startswith(b"\x89PNG") or head.startswith(b"\xff\xd8")):
        raise ValueError("entry.png is neither a PNG nor a JPEG")


def main() -> int:
    source = find_picture()
    check_picture(source)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
