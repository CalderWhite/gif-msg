# gif-msg

gif-msg hides a 128 byte message in a gif while keeping the pixel values identical.
Can you figure out how I did it?

No encryption/compression is implemented out of the box. You can get up to ~256 characters with
a pre computed huffman table or by limiting the charset to 32 unique characters.
The application here is based in the popular use of gifs in online chats.
By selecting a gif as a reaction to something in context the gif is completely natural as opposed
to an encrypted message. Using this tool you can send such messages without looking suspicious.

## Usage

```bash
# hiding the string in the gif.
python3 gif_msg.py encode <infile> <outfile> <string>

# decoding the hidden string in a gif (prints to console)
python3 gif_msg.py decode <infile>
```

## Known Bugs

Greyscale gifs are not currently supported.

## Bugs

Currently PIL is having some issues with certain gifs. Please let me know if you have any issues
or if you have a clue as to the source of PIL's issues. The issue in reference is the manifestation of 
black (or background color) pixels all over the frames. This is simply from opening via `Image.open()`
and saving via `Image.save(filename, save_all=True, append_images=[...])` with no modifications to the image.
