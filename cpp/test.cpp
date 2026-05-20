#include <iostream>
#include <cstdint>

extern "C" {

    int embed_lsb(
        uint8_t* pixels,
        int pixel_count,
        const char* bits,
        int bit_count
    );
}

int main() {

    uint8_t pixels[8] = {
        255, 254, 253, 252,
        251, 250, 249, 248
    };

    const char* bits = "10101010";

    embed_lsb(
        pixels,
        8,
        bits,
        8
    );

    std::cout << "Modified pixels:" << std::endl;

    for (int i = 0; i < 8; i++) 
    {
        std::cout << (int)pixels[i] << " ";
    }
    std::cout << std::endl;
    
    return 0;
}