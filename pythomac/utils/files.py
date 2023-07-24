"""
Adapted from HOMETEL/scripts/python3/utils/files.py under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
"""
import codecs


def get_file_content(fle):
    """ Read fle file.

    This function is modified from HOMETEL/scripts/python3/utils/files.py under the GNU GENERAL PUBLIC LICENSE
        Version 3, 29 June 2007

    @param fle (string) file
    @return ilines (list) content line file
    """
    ilines = []
    src_file = codecs.open(fle, "r", encoding="utf-8")
    for line in src_file:
        ilines.append(line)
    src_file.close()
    return ilines
