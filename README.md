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

- Greyscale gifs are not currently supported.
- Gifs with <256 colors can only hold n//2 bytes, where n=number of colors
- Gifs with duplicate colors in their color palette

**Note**: If there color white (`0xFFFFFF`) is in the color palette and the image has transparency, this will create a duplicate color error since PIL overwrites what is at the transparent index in the palette as `0xFFFFFF`)

## Maintainers
Calder White ([@CalderWhite](https://github.com/CalderWhite))  
_These projects are supported by Calder's [Patreon](https://www.patreon.com/calderwhite). If you enjoyed this project or found it useful, any monetary contributions are greatly appreciated and are put right back into these projects._
