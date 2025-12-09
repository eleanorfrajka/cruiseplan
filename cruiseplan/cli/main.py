#!/usr/bin/env python3
"""
cruiseplan CLI - Modern subcommand architecture for oceanographic cruise planning.
"""

import argparse
import sys
from pathlib import Path


# Define a function stub for later use. This prevents errors if not all imports are available yet.
def download_main():
    """Placeholder for download subcommand logic."""
    print("Download logic will be implemented in cruiseplan.cli.download")


def schedule_main(args: argparse.Namespace):
    """Placeholder for schedule subcommand logic."""
    print(
        f"Schedule logic will process config: {args.config_file} and output to {args.output_dir}"
    )


def stations_main(args: argparse.Namespace):
    """Placeholder for stations subcommand logic."""
    print(f"Stations logic will process bounds: {args.lat}, {args.lon}")


def main():
    """Main CLI entry point following git-style subcommand pattern."""
    parser = argparse.ArgumentParser(
        prog="cruiseplan",
        description="Oceanographic Cruise Planning System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cruiseplan schedule -c cruise.yaml -o results/
  cruiseplan stations --lat 50 65 --lon -60 -30
  cruiseplan download

For detailed help on a subcommand:
  cruiseplan <subcommand> --help
        """,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(
        dest="subcommand",
        title="Available commands",
        description="Choose a subcommand to run",
        help="Available subcommands",
    )

    # --- Download Subcommand ---
    download_parser = subparsers.add_parser(
        "download", help="Download required data assets (bathymetry, etc.)"
    )

    # --- Schedule Subcommand ---
    schedule_parser = subparsers.add_parser(
        "schedule", help="Generate cruise schedule from YAML configuration"
    )
    schedule_parser.add_argument(
        "-c",
        "--config-file",
        required=True,
        type=Path,
        help="YAML cruise configuration file",
    )
    schedule_parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory (default: current)",
    )
    schedule_parser.add_argument(
        "--format",
        choices=["html", "latex", "csv", "kml", "netcdf", "all"],
        default="all",
        help="Output formats (default: all)",
    )
    schedule_parser.add_argument(
        "--validate-depths",
        action="store_true",
        help="Compare stated depths with bathymetry",
    )
    schedule_parser.add_argument("--leg", help="Process specific leg only")

    # --- Stations Subcommand ---
    stations_parser = subparsers.add_parser(
        "stations", help="Interactive station placement with PANGAEA background"
    )
    stations_parser.add_argument(
        "-p", "--pangaea-file", type=Path, help="PANGAEA campaigns pickle file"
    )
    stations_parser.add_argument(
        "--lat",
        nargs=2,
        type=float,
        metavar=("MIN", "MAX"),
        help="Latitude bounds (default: 45 70)",
    )
    stations_parser.add_argument(
        "--lon",
        nargs=2,
        type=float,
        metavar=("MIN", "MAX"),
        help="Longitude bounds (default: -65 -5)",
    )
    stations_parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory (default: current)",
    )
    stations_parser.add_argument(
        "--output-file", type=Path, help="Specific output file path"
    )
    stations_parser.add_argument(
        "--bathymetry-source",
        choices=["etopo2022", "gebco2025"],
        default="etopo2022",
        help="Bathymetry dataset (default: etopo2022)",
    )

    # Parse args
    args = parser.parse_args()

    # Handle case where no subcommand is given
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    # Dispatch to appropriate function
    try:
        # We use dynamic imports here to minimize startup time and only import the
        # necessary module (e.g., cruiseplan.cli.schedule) when its command is run.
        if args.subcommand == "download":
            from cruiseplan.cli.download import main as download_main

            download_main(args)  # Pass args if needed, though 'download' is simple now
        elif args.subcommand == "schedule":
            from cruiseplan.cli.schedule import main as schedule_main

            schedule_main(args)
        elif args.subcommand == "stations":
            from cruiseplan.cli.stations import main as stations_main

            stations_main(args)
        # Add other subcommands as implemented
        else:
            print(f"Subcommand '{args.subcommand}' not yet implemented.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        # A simple catch-all for unexpected errors
        print(f"\n❌ A critical error occurred during execution: {e}")
        # Optionally print traceback if debugging is enabled
        # import traceback; traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
