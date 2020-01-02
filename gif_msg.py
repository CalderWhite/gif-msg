#!/usr/bin/python3
import sys
from PIL import Image, ImageSequence


def decode_palette(encoded_palette):
    """Find the data hidden within the order of the given gct."""
    # python's sort function is lexographic (meaning it takes into consideration
    # the different values within each nested tuple in their order or priority)
    # this way there is always a winner when sorting the array
    # the only edge case where there would be an issue is if there were two colours
    # of the same value, which would be redundant and thus has been eliminated
    # from consideration
    index_ref = sorted(encoded_palette)

    # there will be half as many values as there are in the array since each time
    # you use up an index, one of the lower indexes must be used to complete the byte
    # (think of the gaussian summation theorem proof, if that helps)
    decoded_count = len(encoded_palette) // 2
    decoded = [0] * decoded_count

    # first do the initial values
    for i in range(decoded_count):
        index = encoded_palette.index(index_ref[i])
        decoded[i] = index

        encoded_palette.pop(index)

    # second do the values that are add on to the initial values to get them up to a byte
    for i in range(decoded_count, len(index_ref)):
        index = encoded_palette.index(index_ref[i])
        decoded[decoded_count-1-i] += index

        encoded_palette.pop(index)

    return decoded


def encode_palette(plaintext, palette):
    """Hide the 128 byte list values by specifically ordering the colours in palette."""
    palette.sort()

    encoded_size = len(plaintext) * 2
    encoded = []

    # the half of the colours which have the larger amount of possible indicies
    # one small + one large = len(palette)
    # if the palette is 256 elements long, then small + large = 1 byte
    larges = []
    for i, c in enumerate(plaintext):
        large = min(c, encoded_size - i - 1)
        small = c - large

        larges.append(large)
        encoded.insert(small, palette[ -(i + 1) ])

    # the larges need the most amount of indicies to choose from, so they are 
    # inserted last and in reverse order
    for i in range(len(plaintext)-1, -1, -1):
        encoded.insert(larges[i], palette[i])

    return encoded


def get_palette(im):
    """Helper function to group the palette of im into tuples of 3."""
    grouped_palette = []
    palette = im.getpalette()
    for i in range(0, len(palette), 3):
        grouped_palette += [(palette[i], palette[i+1], palette[i+2])]

    return grouped_palette


def get_unused(palette):
    """Returns an unused color."""
    for r in range(256):
        for g in range(256):
            for b in range(256):
                c = (r, g, b)
                if c not in palette:
                    return c

    # this should never happen
    return None


def encode_gif(in_filename, out_filename, plaintext):
    im = Image.open(in_filename)

    # we must record the new index of transparency since the encoding algorithm
    # will change it. we then tell the PIL to use the new index when saving
    new_transparent = None
    frames = []
    for frame in ImageSequence.Iterator(im):
        palette = get_palette(frame)
        transp_index = frame.info.get("transparency")
        is_transparent = transp_index

        if is_transparent:
            palette[transp_index] = get_unused(palette)

        if len(palette) != 256:
            print("WARNING: Palette size != 256 colors. This may result in issues")
        # This can be supported by deduping the colors and then adding in unique colors
        if len(palette) != len(set(palette)):
            raise Exception("Duplicate colors found in color palette.")

        # pad the input to meet the length of palette
        padded_plaintext = plaintext + "\0" * (len(palette)//2 - len(plaintext))
        plaintext_ints = [ord(i) for i in padded_plaintext]

        # if there is transparency, insert a unique color to represent it
        encoded_gct = encode_palette(plaintext_ints, palette.copy())

        decoded = decode_palette(encoded_gct.copy())
        decoded = [chr(i) for i in decoded]

        print("".join(decoded))


        if is_transparent:
            new_transparent = encoded_gct.index(palette[transp_index])

        new_indicies = [palette.index(i) for i in encoded_gct]
        frames.append(frame.remap_palette(new_indicies))

    if new_transparent is not None:
        frames[0].save(out_filename, format='GIF', save_all=True, transparency=new_transparent,
                       append_images=frames, disposal=0)
    else:
        frames[0].save(out_filename, format='GIF', save_all=True,
                       append_images=frames, disposal=0)


def decode_gif(filename):
    im = Image.open(filename)

    for frame in ImageSequence.Iterator(im):
        palette = get_palette(frame)
        decoded = decode_palette(palette)
        decoded = [chr(i) for i in decoded]

        print("".join(decoded))


def main(args):
    command = args.pop(0) if len(args) > 0 else ""
    if command == "encode":
        encode_gif(*args)
    elif command == "decode":
        plaintext = decode_gif(args[0])
        print(plaintext)
    else:
        print("Unknown command! Commands: encode, decode")


if __name__ == '__main__':
    main(sys.argv[1:])
