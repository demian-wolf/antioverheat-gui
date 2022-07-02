import argparse

from . import PowerManager


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a", "--auto",
        action="store_true",
        help="automatically adjust CPU frequency",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    app = PowerManager(auto_adjust=args.auto)
    app.mainloop()


if __name__ == "__main__":
    main()
