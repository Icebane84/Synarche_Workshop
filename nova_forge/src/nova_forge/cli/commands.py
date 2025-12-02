import argparse
import platform
from typing import List, Optional

# NEW IMPORT
from nova_forge.weaver import CatalystWeaver


def command_status(args: argparse.Namespace) -> None:
    """Reports system health."""
    print("\n[SYNARCHE OPERATIONAL STATUS]")
    print(f"OS Platform:    {platform.system()}")
    print("Nova Forge:     ONLINE")
    print("-----------------------------\n")


# --- NEW HANDLER ---
def command_weave(args: argparse.Namespace) -> None:
    """
    Handler for 'weave' command.
    Generates a prompt bundle from CLI arguments.
    """
    weaver = CatalystWeaver(bundle_name=args.name)

    # Add the main instruction
    weaver.add_process(args.instruction)

    # Generate output
    artifact = weaver.generate()

    if args.output:
        # Save to file
        with open(args.output, "w") as f:
            f.write(artifact)
        print(f"\n[SUCCESS] Catalyst Bundle saved to: {args.output}")
    else:
        # Print to console (for copying)
        print("\n" + "=" * 40)
        print(artifact)
        print("=" * 40 + "\n")


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="synarche")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Status Command
    p_status = subparsers.add_parser("status", help="System health check")
    p_status.set_defaults(func=command_status)

    # --- NEW: Weave Command ---
    p_weave = subparsers.add_parser("weave", help="Generate a prompt context bundle")
    p_weave.add_argument("-n", "--name", required=True, help="Name of the bundle")
    p_weave.add_argument(
        "-i", "--instruction", required=True, help="The core prompt instruction"
    )
    p_weave.add_argument("-o", "--output", help="Optional file path to save output")
    p_weave.set_defaults(func=command_weave)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
