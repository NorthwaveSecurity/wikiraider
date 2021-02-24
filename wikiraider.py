#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2020 Northwave B.V. (www.northwave-security.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import argparse
import logging

# Require Python 3.7
if sys.version_info[0] != 3 or sys.version_info[1] < 7:
    sys.exit('This script requires Python version 3.7 or higher.')

# Ensure requirements are installed
try:
    import colorlog
    import bs4
    import tqdm
    import requests
except:
    sys.exit('Please run `pip3 install -r requirements.txt` first.')

from wikiraider.helpers.PackageHelper import PackageHelper
from wikiraider.actions.ActionList import ActionList
from wikiraider.actions.ActionParse import ActionParse


def require_arguments():
    """Get the arguments from CLI input.

    Returns:
        :class:`argparse.Namespace`: A namespace with all the parsed CLI arguments.

    """

    parser = argparse.ArgumentParser(
        prog=PackageHelper.get_alias(),
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=220, width=220)
    )

    subparsers = parser.add_subparsers(title='actions', dest='action', required=True)

    # create the parser for the "a" command
    parser_list = subparsers.add_parser('list', help='List available databases')
    parser_list.add_argument('-s', '--search', type=str, help='Search on a database name, for example `en` for the English Wikipedia database')

    # create the parser for the "b" command
    parser_parse = subparsers.add_parser('parse', help='Parse a single database')
    parser_parse.add_argument('-u', '--url', type=str, required=True, help='One of the database URLs, for example `https://dumps.wikimedia.org/nlwiki/20200301`')

    return parser.parse_args()


def setup_logger():
    """Setup ColorLog to enable colored logging output."""

    # Colored logging
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "white",
            "SUCCESS": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white"
        }
    ))

    logger = colorlog.getLogger()
    logger.addHandler(handler)

    # Also show INFO logs
    logger.setLevel(logging.INFO)

    # Add SUCCESS logging
    logging.SUCCESS = 25
    logging.addLevelName(
        logging.SUCCESS,
        "SUCCESS"
    )

    setattr(
        logger,
        "success",
        lambda message, *args: logger._log(logging.SUCCESS, message, args)
    )


def print_banner():
    """Print a useless ASCII art banner to make things look a bit nicer."""

    print("""
██╗    ██╗██╗██╗  ██╗██╗██████╗  █████╗ ██╗██████╗ ███████╗██████╗ 
██║    ██║██║██║ ██╔╝██║██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
██║ █╗ ██║██║█████╔╝ ██║██████╔╝███████║██║██║  ██║█████╗  ██████╔╝
██║███╗██║██║██╔═██╗ ██║██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
╚███╔███╔╝██║██║  ██╗██║██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                   
Version """ + PackageHelper.get_version() + """ - Copyright (c) 2020 Northwave B.V. (www.northwave-security.com)
    """)


def main():
    """Start the wordlist parser."""

    print_banner()
    setup_logger()

    args = require_arguments()
    args.cdn = 'https://dumps.wikimedia.org'

    if args.action == 'list':
        ActionList(args).run()

    if args.action == 'parse':
        ActionParse(args).run()


if __name__ == '__main__':
    main()
