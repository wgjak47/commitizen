import io
import os
import sys
import logging
import argparse
import warnings
from decli import cli
from pathlib import Path
from configparser import RawConfigParser, NoSectionError
from commitizen import deafults, commands, out
from commitizen.__version__ import __version__


logger = logging.getLogger(__name__)
data = {
    "prog": "cz",
    "description": (
        "Commitizen is a cli tool to generate conventional commits.\n"
        "For more information about the topic go to "
        "https://conventionalcommits.org/"
    ),
    "formatter_class": argparse.RawDescriptionHelpFormatter,
    "arguments": [
        {"name": "--debug", "action": "store_true", "help": "use debug mode"},
        {"name": ["-n", "--name"], "help": "use the given commitizen"},
        {
            "name": ["--version"],
            "action": "store_true",
            "help": "get the version of the installed commitizen",
        },
    ],
    "subcommands": {
        "title": "commands",
        "commands": [
            {
                "name": "ls",
                "help": "show available commitizens",
                "func": commands.ListCz,
            },
            {
                "name": ["commit", "c"],
                "help": "create new commit",
                "func": commands.Commit,
            },
            {
                "name": "example",
                "help": "show commit example",
                "func": commands.Example,
            },
            {
                "name": "info",
                "help": "show information about the cz",
                "func": commands.Info,
            },
            {"name": "schema", "help": "show commit schema", "func": commands.Schema},
        ],
    },
}


def load_cfg():
    settings = {"name": deafults.NAME}
    config = RawConfigParser("")
    home = str(Path.home())

    config_file = ".cz"
    global_cfg = os.path.join(home, config_file)

    # load cfg from current project
    configs = ["setup.cfg", ".cz.cfg", config_file, global_cfg]
    for cfg in configs:
        if not os.path.exists(config_file) and os.path.exists(cfg):
            config_file = cfg

        config_file_exists = os.path.exists(config_file)
        if config_file_exists:
            logger.debug('Reading file "%s"', config_file)
            config.readfp(io.open(config_file, "rt", encoding="utf-8"))
            log_config = io.StringIO()
            config.write(log_config)
            try:
                settings.update(dict(config.items("commitizen")))
                break
            except NoSectionError:
                # The file does not have commitizen section
                continue

    return settings


def main():
    config = load_cfg()
    parser = cli(data)

    # Show help if no arg provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        raise SystemExit(1)

    args = parser.parse_args()

    if args.name:
        config.update({"name": args.name})

    if args.debug:
        warnings.warn(
            "Debug will be deprecated in next major version. "
            "Please remove it from your scripts"
        )
        logging.getLogger("commitizen").setLevel(logging.DEBUG)

    if args.version:
        out.line(__version__)
        raise SystemExit()

    args.func(config)(args)
