# gif-msg

gif-msg hides a 128 byte message in a gif while keeping the pixel values identical.
Can you figure out how I did it?

No encryption/compression is implemented out of the box. You can get up to ~256 characters with
a pre computed huffman table or by limiting the charset to 32 unique characters.  
GIF's popular usage in messaging apps allow them to blend into conversations naturally.
This way users can send secret (potentially encrypted) messages to eachother without it
being obvious to a 3rd party.

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

Currently PIL has issues handling transparency with gifs. This is simply from opening via `Image.open()`
and saving via `Image.save(filename, save_all=True, append_images=[...])` with no modifications to the image. Tickets tracking this issue include [#1976](https://github.com/python-pillow/Pillow/issues/1976)

## Maintainers
Calder White ([@CalderWhite](https://github.com/CalderWhite))  
_These projects are supported by Calder's [Patreon](https://www.patreon.com/calderwhite). If you enjoyed this project or found it useful, any monetary contributions are greatly appreciated and are put right back into these projects._
