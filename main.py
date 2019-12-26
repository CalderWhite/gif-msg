from PIL import Image


def decode(arr):
    # python's sort function is lexographic (meaning it takes into consideration
    # the different values within each nested tuple in their order or priority)
    # this way there is always a winner when sorting the array
    # the only edge case where there would be an issue is if there were two colours
    # of the same value, which would be redundant and thus has been eliminated 
    # from consideration
    index_table = sorted(arr)

    # there will be half as many values as there are in the array since each time
    # you use up an index, one of the lower indexes must be used to complete the byte
    # (think of the gaussian summation theorem proof, if that helps)
    value_count = len(arr) // 2
    values = [0] * value_count

    # first do the initial values
    for i in range(value_count):
        index = arr.index(index_table[i])
        values[i] = index

        arr.pop(index)

    # second do the values that are add on to the initial values to get them up to a byte
    for i in range(value_count, len(index_table)):
        index = arr.index(index_table[i])
        values[value_count-1-i] += index

        arr.pop(index)

    return values


def encode(values, raw):
    raw.sort()

    # the largest possible value + 1
    enc_max = len(values) * 2
    out = []

    firsts = []
    for i in range(len(values)):

        first = min(values[i], enc_max - i - 1)
        second = values[i] - first

        firsts.append(first)

        out.insert(second, raw[-(i+1)])

    # insert the firsts in reverse order as the first of the firsts must have 
    # the largest list (most indicies) to chose from
    for i in range(len(values)-1, -1, -1):
        out.insert(firsts[i], raw[i])

    return out


def enc_test():
    s = "this is a test"
    # the padding is required since the max value is dictated by the length of the list
    s += "\0" * (128 - len(s))
    values = [ord(i) for i in s]

    im = Image.open("source.gif")
    palette = []
    _p = im.getpalette()
    for i in range(0, len(_p), 3):
        palette += [(_p[i], _p[i+1], _p[i+2])]
    encoded_gct = encode(values, palette.copy())

    new_indicies = [palette.index(i) for i in encoded_gct]

    frames = []
    for i in range(im.n_frames):
        frames.append(im.remap_palette(new_indicies))
        im.seek(i)

    # POST REMAP ################################
    frames[0].save("out.gif", save_all=True, append_images=frames)

def dec_test():
    im = Image.open("out.gif")
    palette = []
    _p = im.getpalette()
    for i in range(0, len(_p), 3):
        palette += [(_p[i], _p[i+1], _p[i+2])]

    #print("Decoded:", palette)

    decoded = decode(palette)
    #print(decoded)
    decoded = [chr(i) for i in decoded]
    print("".join(decoded))

enc_test()
dec_test()
