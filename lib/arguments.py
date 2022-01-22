import argparse

def arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--username", metavar="", type=str, default="port0001", help="Generated account's username."
        )
    parser.add_argument(
        "--password", metavar="", type=str, default="H4x0rSqu4d1337", help="Password of the accounts."
        )
    parser.add_argument(
        "--invite", metavar="", type=str, required=True, help="Server invite the accounts join on creation."
        )
    parser.add_argument(
        "--threads", metavar="", type=int, default=50, help="Amount of threading while creating accounts."
        )
    parser.add_argument(
        "--workers", metavar="", type=int, default=5, help="Amount of workers while creating accounts."
        )
    parser.add_argument(
        "--proxies", metavar="", type=str, required=True, help="Choose to use proxies or not (\"y\", \"n\")"
        )

    return parser.parse_args()
