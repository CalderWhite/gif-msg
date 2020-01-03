# gif-msg

gif-msg hides a 128 byte message in a gif while keeping the pixel values identical.
Can you figure out how I did it?

GIF's popular usage in messaging apps allow them to blend into conversations naturally.
This way users can send secret (potentially encrypted) messages to eachother without it
being obvious to a 3rd party.

## Usage

```
usage: gif_msg.py [-h] [--key KEY] [--compress]
                  command infile [outfile] [body]

Encode/Decode 128 bytes into a gif file.

positional arguments:
  command     The command to be run (encode/decode)
  infile      The input gif.
  outfile     The outfile gif. (applicable for encode)
  body        The message to be encoded. (applicable for encode)

optional arguments:
  -h, --help  show this help message and exit
  --key KEY   If given a key, AES will be used to encrypt/decrypt the message
              body.
  --compress  If supplied, a pre computed huffman table will be used to
              compress the message body. NOTE: This will not always result in
              positive compression since the huffman table is pre computed.
```

## Known Bugs

- Greyscale gifs are not currently supported.
- Gifs with <256 colors can only hold n//2 bytes, where n=number of colors
- Gifs with duplicate colors in their color palette

**Note**: If there color white (`0xFFFFFF`) is in the color palette and the image has transparency, this will create a duplicate color error since PIL overwrites what is at the transparent index in the palette as `0xFFFFFF`)

## Maintainers
Calder White ([@CalderWhite](https://github.com/CalderWhite))  
_These projects are supported by Calder's [Patreon](https://www.patreon.com/calderwhite). If you enjoyed this project or found it useful, any monetary contributions are greatly appreciated and are put right back into these projects._
