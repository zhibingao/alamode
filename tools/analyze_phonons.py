#!/usr/bin/env python
#
# analyze_phonons.py
#
# Simple interface to the command line script "analyze_phonons.cpp".
#
# Copyright (c) 2014 Terumasa Tadano
#
# This file is distributed under the terms of the MIT license.
# Please see the file 'LICENCE.txt' in the root directory
# or http://opensource.org/licenses/mit-license.php for information.
#
"""
This python script is a simple user interface to
the C++ analyzer program "analyze_phonons.cpp".
To execute this script, the above c++ program has to be
compiled and made executable.
"""
import sys
import os
import optparse
import subprocess

parser = optparse.OptionParser()
parser.add_option('--temp', help="target temperature to analyze")
parser.add_option('--mode', help="specify phonon mode index to print")
parser.add_option('--kpoint', help="specify k-point index to print")

parser.add_option('--calc', metavar='tau|kappa|cumulative',
                  help=('specify what to print. Available options are '
                        'tau (Lifetime, mean-free-path, etc.), '
                        'kappa (Thermal conductivity), and '
                        'cumulative (Cumulative thermal conductivity). '
                        'When --calc=cumulative, please specify the '
                        '--direction option.'))

parser.add_option('--noavg', action="store_false", dest="average_gamma",
                  default=True, help="do not average the damping function \
at degenerate points")

group = optparse.OptionGroup(parser,
                             "The following options are available/necessary \
when --calc=cumulative ")

group.add_option('--length', metavar="Lmax:dL",
                 help="specify the maximum value of system size L and its \
step dL in units of nm. \
The default value is --length=1000:10 .")

group.add_option('--direction', metavar="1|2|3", help="specify which \
direction (xyz) to consider the size effect. \
When --direction=1 (2, 3), phonon mean-free-paths (ell) \
along x (y, z) are compared with the system size L. Then, \
the cumulative thermal conductivity is calculated by considering \
phonon modes satisfying ell <= L.")

parser.add_option_group(group)

options, args = parser.parse_args()
file_result = args[0]

dir_obj = os.path.dirname(__file__)
analyze_obj = dir_obj + "/analyze_phonons "


def print_temperature_dep_lifetime():

    if options.kpoint is None or options.mode is None:
        sys.exit("Please specify the temperature by --temp option, \
or specify both --kpoint and --mode when --calc=tau")
    else:
        if len(options.kpoint.split(':')) != 1:
            sys.exit("Invalid usage of --kpoint for --calc=tau")
        if len(options.mode.split(':')) != 1:
            sys.exit("Invalid usage of --mode for --calc=tau")

        target_k = int(options.kpoint)
        target_s = int(options.mode)
        calc = "tau_temp"
        command = analyze_obj + file_result + " " + calc + " " + avg \
            + " " + str(target_k) + " " + str(target_s)

        subprocess.call(command, shell=True)


def print_lifetime_at_given_temperature():

    if options.kpoint is None:
        beg_k = 1
        end_k = 0
    else:
        if len(options.kpoint.split(':')) == 1:
            beg_k = int(options.kpoint)
            end_k = beg_k
        elif len(options.kpoint.split(':')) == 2:
            arr = options.kpoint.split(':')
            beg_k, end_k = int(arr[0]), int(arr[1])
        else:
            sys.exit("Invalid usage of --kpoint for --calc=tau")

    if options.mode is None:
        beg_s = 1
        end_s = 0
    else:
        if len(options.mode.split(':')) == 1:
            beg_s = int(options.mode)
            end_s = beg_s
        elif len(options.mode.split(':')) == 2:
            arr = options.mode.split(':')
            beg_s, end_s = int(arr[0]), int(arr[1])
        else:
            sys.exit("Invalid usage of --mode for --calc=tau")

    command = analyze_obj + file_result + " " + calc + " " + avg + " "\
        + str(beg_k) + " " + str(end_k) + " "\
        + str(beg_s) + " " + str(end_s) + " " + options.temp

    subprocess.call(command, shell=True)


def print_thermal_conductivity():

    if not (options.kpoint is None):
        print "# Warning: --kpoint option is discarded"

    if options.mode is None:
        beg_s = 1
        end_s = 0
    else:
        if len(options.mode.split(':')) == 1:
            beg_s = int(options.mode)
            end_s = beg_s
        elif len(options.mode.split(':')) == 2:
            arr = options.mode.split(':')
            beg_s, end_s = int(arr[0]), int(arr[1])
        else:
            sys.exit("Invalid usage of --mode for --calc=kappa")

    command = analyze_obj + file_result + " " + calc + " " + avg\
        + " " + str(beg_s) + " " + str(end_s)

    subprocess.call(command, shell=True)


def print_cumulative_thermal_conductivity():

    if options.temp is None:
        sys.exit("--temp is necessary when --calc=cumulative")

    if not (options.kpoint is None):
        print "# Warning: --kpoint option is discarded"

    if options.mode is None:
        beg_s = 1
        end_s = 0
    else:
        if len(options.mode.split(':')) == 1:
            beg_s = int(options.mode)
            end_s = beg_s
        elif len(options.mode.split(':')) == 2:
            arr = options.mode.split(':')
            beg_s, end_s = int(arr[0]), int(arr[1])
        else:
            sys.exit("Invalid usage of --mode for --calc=cumulative")

    if options.length is None:
        max_len = 1000.0
        d_len = 1.0
    elif len(options.length.split(':')) == 2:
        arr = options.length.split(':')
        max_len, d_len = float(arr[0]), float(arr[1])
    else:
        sys.exit("Invalid usage of --length option")

    size_flag = [0]*3

    if options.direction is None:
        for i in range(3):
            size_flag[i] = 0
    else:
        if len(options.direction.split(':')) > 3:
            sys.exit("Invalid usage of --direction")

        arr = options.direction.split(':')
        for i in range(len(options.direction.split(':'))):
            size_flag[int(arr[i])-1] = 1

    command = analyze_obj + file_result + " " + calc + " " + avg + " "\
        + str(beg_s) + " " + str(end_s) + " " + str(max_len) + " "\
        + str(d_len) + " " + options.temp + " " + str(size_flag[0]) \
        + " " + str(size_flag[1]) + " " + str(size_flag[2])

    subprocess.call(command, shell=True)


if __name__ == '__main__':

    calc = options.calc

    if options.average_gamma:
        avg = "1"
    else:
        avg = "0"

    # Compute phonon lifetimes, mean-free-path,
    # and mode-decomposed thermal conductivity
    if calc == "tau":

        # When --temp option is not specified, print temperature dependence
        # of phonon lifetimes at given mode and k point.
        if options.temp is None:
            print_temperature_dep_lifetime()

        # When --temp option is specified, print phonon lifetimes and
        # other quantities at the specified temperature.
        else:
            print_lifetime_at_given_temperature()

    elif calc == "kappa":
        print_thermal_conductivity()

    # Compute cumulative thermal conductivity.
    elif calc == "cumulative":
        print_cumulative_thermal_conductivity()

    else:
        sys.exit("Invalid --calc option given")
