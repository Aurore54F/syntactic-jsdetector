# Copyright (C) 2019 Aurore Fass
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
    Utility file, stores shared information.
"""

import os
import timeit
import logging
import sys

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.setrecursionlimit(400000)
NUM_WORKERS = 2


class UpperThresholdFilter(logging.Filter):
    """
    This allows us to set an upper threshold for the log levels since the setLevel method only
    sets a lower one
    """

    def __init__(self, threshold, *args, **kwargs):
        self._threshold = threshold
        super(UpperThresholdFilter, self).__init__(*args, **kwargs)

    def filter(self, rec):
        return rec.levelno <= self._threshold


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)
LOGGER = logging.getLogger()
LOGGER.addFilter(UpperThresholdFilter(logging.CRITICAL))


def micro_benchmark(message, elapsed_time):
    """ Micro benchmarks. """
    logging.info('%s %s%s', message, str(elapsed_time), 's')
    return timeit.default_timer()


def parsing_commands(parser):
    """
        Filling of an ArgumentParser object to later parse the command line into Python data types.

        -------
        Parameter:
        - parser: ArgumentParser
            Parser to fill.

        -------
        Returns:
        - ArgumentParser
            Parser filled.
    """

    parser.add_argument('--v', metavar='VERBOSITY', type=int, nargs=1, choices=[0, 1, 2, 3, 4, 5],
                        default=[2], help='controls the verbosity of the output, from 0 (verbose) '
                                          + 'to 5 (less verbose)')
    parser.add_argument('--analysis_path', metavar='DIR', type=str, nargs=1,
                        default=[os.path.join(SRC_PATH, 'Analysis')],
                        help='folder to store the features\' analysis results in')

    return parser


def control_logger(logging_level):
    """
        Builds a logger object.

        -------
        Parameter:
        - logging_level: int
            Verbosity of the logging. Between 0 and 5.
    """

    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.getLevelName(logging_level * 10))
