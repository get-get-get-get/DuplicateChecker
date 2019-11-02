#!/usr/bin/env python3



def main():
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
            "template",
            help="Put help here"
    )

    args = parser.parse_args()

    main()
