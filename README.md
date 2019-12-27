# gif-msg

Hides a 128 byte message in a gif. The input and output's pixels are identical.  
Can you figure out how I did it?

No encryption/compression out of the box. You can get up to ~256 characters with
a pre computed huffman table or limiting the charset to 32 unique characters.

## Usage

```bash
# hiding the string in the gif.
python3 gif_msg.py encode <infile> <outfile> <string>

# decoding the hidden string in a gif (prints to console)
python3 gif_msg.py decode <infile>
```
