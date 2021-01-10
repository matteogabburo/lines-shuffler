import sys
import os
import argparse
import mmap
import random
from tqdm import tqdm

def get_fmap(pth_file):
    """Open a mmap-ped file"""

    f = open(pth_file, "r+")
    return mmap.mmap(f.fileno(), 0)

def get_lines_positions(fmap):
    """Return the mmap indexes that identify the lines in the mmap"""

    positions = [0]
    while fmap.readline():
        positions.append(fmap.tell())
    # remove the las positions, since it index the end of the eof 
    return positions[:-1]
    
def get_line(fmap, pos):
    """Return a single line according with the mmap position computed by ```get_lines_positions```"""

    fmap.seek(pos)
    return fmap.readline()

def main(args):

    # some checks of the inputs
    if not os.path.exists(args.path_in):
        raise FileNotFoundError(r"The input file does not exist")

    # get the inuput file mmap-ped
    fmap = get_fmap(args.path_in)

    # get the number of lines of the input file
    print('Mapping lines...')
    positions = get_lines_positions(fmap)

    # set the seed, if None the seed used will be the current time (see random docs)
    random.seed(a=args.seed)

    # prepare the shuffled positions list
    random.shuffle(positions)

    # writing
    print('Writing the suffled file in "{}"...'.format(args.path_out))
    with open(args.path_out, "wb") as fout:
        for pos in tqdm(positions):
            fout.write(get_line(fmap, pos))

if __name__ == "__main__":
    try:

        parser = argparse.ArgumentParser(description="A simple tool that can be used to shuffle the lines of a document.")
        parser.add_argument("-i", "--path_in", type=str, required=True, help="The input file")
        parser.add_argument("-o", "--path_out", type=str, required=True, help="The output file")

        parser.add_argument("-s", "--seed", type=int, default=None, help="The random seed")

        args = parser.parse_args()
        sys.exit(main(args))

    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")
        pass
