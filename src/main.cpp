#include <iostream>
#include <boost/dynamic_bitset.hpp>
#include <map>

#include "HuffmanCode.h"

/*
extern "C" {
    #include "third_party/gifenc/gifenc.h"
}
*/

// pre compute huffman code table for text messages
const std::map<char, HuffmanCode> HUFF_CODES = {
    { ' ',  { 0b111, 3 } },
    { '\n', { 0b011, 3 } },
    { 'e',  { 0b1100, 4 } },
    { 't',  { 0b1010, 4 } },
    { 'o',  { 0b1000, 4 } },
    { 'a',  { 0b0100, 4 } },
    { 'i',  { 0b0011, 4 } },
    { 's',  { 0b0000, 4 } },
    { 'h',  { 0b11011, 5 } },
    { 'n',  { 0b10111, 5 } },
    { 'r',  { 0b10011, 5 } },
    { 'u',  { 0b01011, 5 } },
    { 'l',  { 0b00100, 5 } },
    { 'd',  { 0b00101, 5 } },
    { 'm',  { 0b00010, 5 } },
    { 'g',  { 0b110100, 6 } },
    { 'y',  { 0b101100, 6 } },
    { 'k',  { 0b100101, 6 } },
    { 'f',  { 0b100100, 6 } },
    { 'p',  { 0b010101, 6 } },
    { 'w',  { 0b000111, 6 } },
    { 'b',  { 0b010100, 6 } },
    { 'v',  { 0b1101011, 7 } },
    { 'c',  { 0b1101010, 7 } },
    { '\'', { 0b10110111, 8 } },
    { '.',  { 0b00011000, 8 } },
    { 'z',  { 0b00011001, 8 } },
    { 'j',  { 0b101101011, 9 } }
};

void encodeStr(std::string& input) {
    int total = 0;
    for (char s : input) {
        total += HUFF_CODES.at(s).len;
    }

    std::cout << (1 + total/8) << " bytes " << total << " bits\n";
}

int main(int argc, char* argv[]) {
    //std::string s = "i think this is a reasonable size for your average message. "
    //                "its about two sentances long on average.";
    std::string s;
    std::getline(std::cin, s);

    encodeStr(s);
}
