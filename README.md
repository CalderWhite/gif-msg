# gif-msg

gif-msg hides a 128 byte message in a gif while keeping the pixel values identical.
Can you figure out how I did it?

No encryption/compression is implemented out of the box. You can get up to ~256 characters with
a pre computed huffman table or by limiting the charset to 32 unique characters.

## Usage

```bash
# hiding the string in the gif.
python3 gif_msg.py encode <infile> <outfile> <string>

# decoding the hidden string in a gif (prints to console)
python3 gif_msg.py decode <infile>
```
