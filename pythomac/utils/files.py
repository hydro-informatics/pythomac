"""
Adapted from HOMETEL/scripts/python3/utils/files.py under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
"""


def get_file_content(fle):
    """ Read the fle file into a list of lines.

    This function is modified from HOMETEL/scripts/python3/utils/files.py under the GNU GENERAL PUBLIC LICENSE
        Version 3, 29 June 2007

    @param fle (string) file
    @return ilines (list) content line file
    """
    with open(fle, "r", encoding="utf-8") as src_file:
        return src_file.readlines()
