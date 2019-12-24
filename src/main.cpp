#include <iostream>
#include <bitset>
#include <math.h>

/*
extern "C" {
    #include "third_party/gifenc/gifenc.h"
}
*/

// the amount of bits to describe one character
const int CHAR_WIDTH = 5;

/*
 * A list of index to index matching. The input index is the char that is to be 
 * mapped. The output is the index of that char in the LEGAL_CHARS.
 * 255 represents out of bounds.
 */
const unsigned char CHAR_TABLE[] = {
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
    0xFF, 0xFF, 0x1a, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, // maps ' ' --> 26
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x1b, 0xFF, 0xFF, 0xFF, // maps '.' --> 27
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x01, 0x02, // maps 'a' --> 0, 'b' --> 1 [...]
    0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, // through a-z
    0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 
    0x17, 0x18, 0x19, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
};

const char LEGAL_CHARS[] = {
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '.'
};


/**
 * This function assumes that all the characters included are legal.
 */
inline int getEncodedLen(std::string s) {
    return 1 + (s.length() * 5) / 8;
}

inline unsigned char charToIndex(char c) {
    return CHAR_TABLE[static_cast<unsigned char>(c)];
}

inline char indexToChar(unsigned char i) {
    return LEGAL_CHARS[i];
}

void encodeStr(char out[], std::string& s) {
    unsigned char bytes_out[(s.length()*5) + 1] = {0};
    for (int i=0; i<s.length(); i++) {
        bytes_out[i] = charToIndex(s[i]);
    }

    int byte_index = -1;
    int char_index = -1;
    for (int i=0; i<s.length()*5; i++) {
        int bit_index = i % 8;
        int char_bit = i % 5;

        if (bit_index == 0) {
            ++byte_index;
        }
        if (char_bit == 0) {
            ++char_index;
        }

        int bit = ((bytes_out[char_index] & (1 << char_bit)) >> char_bit);
        out[byte_index] |= bit << bit_index;

    }
}

void decodeStr(char input[], char output[], int input_len) {
    char buffer = 0;
    int byte_index = 0;
    int char_index = 0;
    for (int i=0; i<input_len*8; i++) {
        int bit_index = i % 8;
        int char_bit = i % 5;

        if (bit_index == 0 && i != 0) {
            ++byte_index;
        }
        if (char_bit == 0 && i != 0) {
            output[char_index] = indexToChar(buffer);

            ++char_index;
            buffer = 0;
        }

        int bit = ((input[byte_index] & (1 << bit_index)) >> bit_index);
        buffer |= bit << char_bit;
    }
}

int main(int argc, char* argv[]) {
    std::string s = "this is a mega bruh moment my dude.";
    char out[getEncodedLen(s)] = {0};
    encodeStr(out, s);

    char dec[s.length()];
    decodeStr(out, dec, getEncodedLen(s));
    std::cout << dec << "\n";
}
