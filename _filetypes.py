'''

This stores all possible selection conditions and its associated file extensions

'''

import magic
import eyed3
import math

def condition_check(type, path):
    # ext
    if type.startswith("ext:"): return condition_check_by_ext(type.split(":", 1)[1], path)
    # type
    elif type.startswith("type:"): return condition_check_by_type(type.split(":", 1)[1], path)
    # eyed3
    elif type.startswith("eyed3:"): return condition_check_by_eyed3(type.split(":", 1)[1], path)
    # generic
    elif type == "any file": return True
    elif type == "none": return False
    # could not validate
    else: return False

# checks for file extension
def condition_check_by_ext(string, path):
    return path.endswith(string)

# checks for fily tipe with magic
def condition_check_by_type(string, path):
    return magic.Magic(mime=True).from_file(path).startswith(string)

# checks for mp3 tags with eyed3
def condition_check_by_eyed3(string, path):
    if not path.endswith(".mp3"): return False # can only verify mp3 files

    try:
        file = eyed3.load(path)
        if string.startswith("rating:"):
            return math.ceil(file.tag.frame_set[b'POPM'][0].rating / 51) >= int(string.split(":", 1)[1])

        return False
    except:
        return False