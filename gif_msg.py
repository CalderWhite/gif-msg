#!/usr/bin/python3
import argparse
import io
import subprocess
import sys

from PIL import Image, ImageSequence
from simple_aes_cipher.simple_aes_cipher import AESCipher, generate_secret_key
from PySmaz import smaz


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
    # (think of the arithmetic summation formula proof, if that helps)
    # https://www.purplemath.com/modules/series6.htm
    decoded_count = len(encoded_palette) // 2
    decoded = [0] * decoded_count

    # first do the initial values
    for i in range(decoded_count):
        index = encoded_palette.index(index_ref[i])
        decoded[i] = index

        encoded_palette.pop(index)

    # second do the values that are added on to the initial values to get them up to a byte
    for i in range(decoded_count, len(index_ref)):
        index = encoded_palette.index(index_ref[i])
        decoded[decoded_count-1-i] += index

        encoded_palette.pop(index)

    return decoded


def encode_palette(plaintext, palette):
    """Hide the 128 byte list values by specifically ordering the colours in the palette."""
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


def encode_gif(im, plaintext):
    """Encodes the plaintext into the given GIF (im) and returns the bytes of the encoded GIF."""
    # we must record the new index of transparency since the encoding algorithm
    # will change it. we then tell the PIL to use the new index when saving
    new_transparent = None
    frames = []
    for frame in ImageSequence.Iterator(im):
        palette = get_palette(frame)
        transp_index = frame.info.get("transparency")
        is_transparent = transp_index

        # if there is transparency, set the index to a unique color to represent it
        if is_transparent:
            palette[transp_index] = get_unused(palette)

        if len(palette) != 256:
            print("WARNING: Palette size != 256 colors. This may result in issues")
        # This can be supported by deduping the colors and then adding in unique colors
        if len(palette) != len(set(palette)):
            raise Exception("Duplicate colors found in color palette.")

        # pad the input to meet the length of palette
        padding = b"\0" * (len(palette)//2 - len(plaintext))
        padded_plaintext = b"".join([plaintext, padding])
        encoded_gct = encode_palette(padded_plaintext, palette.copy())

        if is_transparent:
            new_transparent = encoded_gct.index(palette[transp_index])

        new_indicies = [palette.index(i) for i in encoded_gct]
        frames.append(frame.remap_palette(new_indicies))

    bytes_out = io.BytesIO()
    if new_transparent is not None:
        frames[0].save(bytes_out, format='GIF', save_all=True, transparency=new_transparent,
                       append_images=frames, disposal=0)
    else:
        frames[0].save(bytes_out, format='GIF', save_all=True,
                       append_images=frames, disposal=0)

    bytes_out.seek(0)

    # re-encode the binary data with gifsicle since its encoder uses compression
    proc = subprocess.Popen('gifsicle', stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    proc.stdin.write(bytes_out.read())
    proc.stdin.flush()
    proc.stdin.close()

    return proc.stdout


def decode_gif(im):
    """Decodes the given GIF (im)."""
    palette = get_palette(im)
    decoded = decode_palette(palette)

    return bytes(decoded)


def copy_bytes_to_file(src, dst, bufsize=16384):
    while True:
        buf = src.read(bufsize)
        if not buf:
            break
        dst.write(buf)

def encrypt_AES(plaintext, key):
    key = generate_secret_key(key)
    cipher = AESCipher(key)

    return cipher.encrypt(plaintext)


def decrypt_AES(ciphertext, key):
    key = generate_secret_key(key)
    cipher = AESCipher(key)

    return cipher.decrypt(ciphertext)


def main(args):
    parser = argparse.ArgumentParser(description="Encode/Decode 128 bytes"
                                     " into a gif file.")
    parser.add_argument("command", type=str, help="The command to be run (encode/decode)")
    parser.add_argument("infile", type=str, help="The input gif.")
    parser.add_argument("outfile", type=str, help="The outfile gif. (applicable for encode)",
                        nargs='?')
    parser.add_argument("body", type=str, help="The message to be encoded. "
                        " (applicable for encode)", nargs='?')

    parser.add_argument("--key", type=str, default=None,
                        help="If given a key, AES will be used to encrypt/decrypt the message body.")
    parser.add_argument("--compress", const=True, action="store_const",
                        help="If supplied, smaz will be used to"
                        " compress the body. NOTE: This is only effective with"
                        " language, and binary data is best left uncompressed")

    args = parser.parse_args()

    use_crypto = args.key is not None
    use_compress = args.compress is not None

    if args.command == "encode":
        if args.body is None or args.outfile is None:
            parser.error("outfile and body are required for encoding.")

        im = Image.open(args.infile)

        if use_compress:
            body = smaz.compress(args.body)
        else:
            body = args.body

        print(len(body))

        if use_crypto:
            body = encrypt_AES(body, args.key)
        else:
            body = body.encode('utf-8')

        bytes_out = encode_gif(im, body)

        with open(args.outfile, 'wb') as w:
            copy_bytes_to_file(bytes_out, w)
    elif args.command == "decode":
        im = Image.open(args.infile)
        body = decode_gif(im)

        if use_crypto:
            plaintext = decrypt_AES(body, args.key)
        else:
            plaintext = body

        if use_compress:
            plaintext = smaz.decompress(plaintext.decode('utf-8'))

            print(plaintext)
        else:
            sys.stdout.buffer.write(plaintext)
            sys.stdout.buffer.flush()

            # add a newline after the raw bytes
            print()


if __name__ == '__main__':
    main(sys.argv[1:])
