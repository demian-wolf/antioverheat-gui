import argparse

from . import OverheatNotification


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", "--sound",
        action="store_true",
        default=True,
        help="enable sound notification",
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=500,
        help="interval (ms) for frequency retrieval",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    app = OverheatNotification(
        sound=args.sound,
        interval=args.interval,
    )
    app.mainloop()


if __name__ == "__main__":
    main()
