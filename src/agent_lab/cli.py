from __future__ import annotations

import argparse

from agent_lab import __version__


def _maybe_load_dotenv() -> None:
    """Optional: establish the .env convention early without making it a hard dependency."""
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return
    load_dotenv()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agent-lab", description="Swarm ladder CLI (L0).")
    p.add_argument("--version", action="store_true", help="Print version and exit.")
    sub = p.add_subparsers(dest="cmd", required=False)

    hello = sub.add_parser("hello", help="Say hello deterministically.")
    hello.add_argument("name", nargs="?", default="world")
    return p


def main(argv: list[str] | None = None) -> int:
    _maybe_load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    if args.cmd == "hello":
        print(f"hello {args.name}")
        return 0

    parser.print_help()
    return 0
