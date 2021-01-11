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

def get_lines_positions(fmap, bucket_size=1):
    """Return the mmap indexes that identify the lines in the mmap. Bucket_size is the the number of lines that each bucket should contain"""

    positions = [[0, 1]]
    bucket_counter = 1
    while fmap.readline():
        if bucket_counter % bucket_size == 0:
            positions.append([fmap.tell(), 1])
        else:
            positions[-1][1] += 1
        bucket_counter += 1

    # remove the las positions, since it index the end of the eof 
    return positions
    
def get_line(fmap, pos):
    """Return a single line according with the mmap position computed by ```get_lines_positions```"""

    fmap.seek(pos)
    return fmap.readline()

def get_bucket(fmap, pos, bucket_size):
    """Return a all the lines of a bucket according with the mmap position computed by ```get_lines_positions```"""

    fmap.seek(pos)
    for _ in range(bucket_size):
        yield fmap.readline()

def main(args):

    # some checks of the inputs
    if not os.path.exists(args.path_in):
        raise FileNotFoundError(r"The input file does not exist")

    # get the inuput file mmap-ped
    fmap = get_fmap(args.path_in)

    # get the number of lines of the input file
    print('Mapping lines...')
    positions = get_lines_positions(fmap, args.bucket_size)

    # set the seed, if None the seed used will be the current time (see random docs)
    random.seed(a=args.seed)

    # prepare the shuffled positions list
    random.shuffle(positions)

    # writing
    print('Writing the suffled file in "{}"...'.format(args.path_out))
    with open(args.path_out, "wb") as fout:
        buckets_buffer = []
        for pos, bucket_size in tqdm(positions):
            
            buckets_buffer.append([line for line in get_bucket(fmap, pos, bucket_size)])

            if len(buckets_buffer) > args.buffer_size:
                for bucket in buckets_buffer:
                    for line in bucket:
                        fout.write(line)
                buckets_buffer = []

        # write if something remains in the buffer
        if len(buckets_buffer) > 0:
            for bucket in buckets_buffer:
                    for line in bucket:
                        fout.write(line)

if __name__ == "__main__":
    try:

        parser = argparse.ArgumentParser(description="A simple tool that can be used to shuffle the lines of a document.")
        parser.add_argument("-i", "--path_in", type=str, required=True, help="The input file.")
        parser.add_argument("-o", "--path_out", type=str, required=True, help="The output file.")

        parser.add_argument("-bs", "--bucket_size", type=int, default=1, help="The number of line for each bucket. To be use to shuffle huge files.")
        parser.add_argument("-bf", "--buffer_size", type=int, default=1, help="The size of the writing buffer in terms of buckets.")
        parser.add_argument("-s", "--seed", type=int, default=None, help="The random seed.")
        

        args = parser.parse_args()
        sys.exit(main(args))

    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")
        pass
