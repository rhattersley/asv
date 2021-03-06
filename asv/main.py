# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import sys

import six

from . import commands
from .config import Config
from .console import log
from .plugin_manager import plugin_manager
from . import util


def main():
    parser, subparsers = commands.make_argparser()

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    log.enable(args.verbose)

    # Use the path to the config file as the cwd for the remainder of
    # the run
    dirname = os.path.dirname(os.path.abspath(args.config))
    os.chdir(dirname)

    try:
        result = args.func(args)
    except (RuntimeError, util.UserError) as e:
        log.error(six.text_type(e))
        sys.stdout.write('\n')
        sys.exit(1)

    sys.stdout.write('\n')

    if result is None:
        result = 0

    sys.exit(result)
