#!/usr/bin/env python

"""format_exclusions.py: Formats excluded tests in .ini files. (Width and alphabetical order).
    Makes ugly files that have exclusions listed in one long line more readable and workable.

Usage:
    This should be called by a hook before the test run.
    Must reside in <sdk_repo>/tdvt/tdvt
    ./format_exclusions.py

Author:
    Stephen Davis - 5/6/2023
"""

import os


def format_exclusions(directory):
    """
    Ensure that the excluded tests are not contained on one line
    and instead placed on multiple lines, observing an 80 max width.
    :param directory: Path to directory containing .ini files.
    :return:
    """
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        # checking if it is a file
        if os.path.isfile(filepath):
            os.chmod(filepath, 0o600)
            with open(filepath, 'r+') as f:
                lines = f.readlines()
                # check for lines containing exclusions over 80 characters
                for i, line in enumerate(lines):
                    if 'Exclusions' in line and len(line) > 80:
                        name, exclusions = line.split('=')
                        # create the list of exclusions
                        exclusions = exclusions.split(',')
                        exclusions = [x.strip() for x in exclusions]
                        # we append to a wrapped exclusions list
                        wrapped_exclusions = []
                        current_line = name + '= '  # include the trailing space after '='
                        # sort the exclusions in ascending order
                        exclusions.sort()
                        # add & check width of current line with each addition
                        for exclusion in exclusions:
                            exclusion = exclusion.strip()
                            if len(current_line) + len(exclusion) + 2 > 80:
                                wrapped_exclusions.append(current_line.rstrip())
                                # we indent the exclusions that don't fit on original line
                                current_line = '    ' + exclusion + ','
                            else:
                                if current_line == name + '= ':
                                    current_line += exclusion + ', '
                                else:
                                    current_line += exclusion + ', '
                        # remove the comma from the last exclusion
                        wrapped_exclusions.append(current_line.rstrip(', '))

                        # replace the line with the formatted exclusions
                        lines[i] = '\n'.join(wrapped_exclusions) + '\n'

                # write the modified lines back to the file
                f.seek(0)
                f.writelines(lines)
                f.truncate()

            # set the file permissions back to read-only
            os.chmod(filepath, 0o444)


if __name__ == '__main__':
    dir_path = os.getcwd() + "/config"
    format_exclusions(dir_path)