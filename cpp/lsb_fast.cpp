#include <cstring>
#include <cstdint>

extern "C" 
{
    /*
     * Embed bits into pixel array using LSB
     */

    int embed_lsb(
        uint8_t* pixels,
        int pixel_count,
        const char* bits,
        int bit_count
    ) {

        if (bit_count > pixel_count) {

            return -1;
        }

        for (int i = 0; i < bit_count; i++) {

            pixels[i] =
                (pixels[i] & 0xFE)
                | (bits[i] - '0');
        }

        return 0;
    }


    /*
     * Extract LSB bits
     */

    void extract_lsb(
        const uint8_t* pixels,
        int pixel_count,
        char* output,
        int extract_count
    ) {

        int count =
            extract_count < pixel_count
            ? extract_count
            : pixel_count;

        for (int i = 0; i < count; i++) {

            output[i] =
                '0' + (pixels[i] & 1);
        }

        output[count] = '\0';
    }


    /*
     * LSB randomness score
     */

    double lsb_randomness_score(
        const uint8_t* pixels,
        int pixel_count
    ) {

        if (pixel_count == 0) {

            return 0.0;
        }

        int ones = 0;

        for (int i = 0; i < pixel_count; i++) {

            ones += (pixels[i] & 1);
        }

        return (double)ones / pixel_count;
    }

}