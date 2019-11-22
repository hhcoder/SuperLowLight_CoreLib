#include "gauss_pyramid.h"

#include <stdexcept>
#include <iostream>

class AiSnsMain
{
public:
    AiSnsMain(const RawFormat& in_raw_format)
        :   raw_format(in_raw_format),
            max_num_raws(14), 
            gauss_pyramid(raw_format, max_num_raws)
    {
    }

private:
    RawFormat raw_format;
    unsigned max_num_raws;
    GaussianPyramid gauss_pyramid;
};

int AiSuperNightShotInit(
    const RawFormat* in_raw_format,
    ai_super_night_shot_handle_t* out_h, 
    size_t* out_max_num_raws)
{
    if (nullptr==in_raw_format || nullptr==out_h || nullptr==out_max_num_raws)
        return AI_SUPER_NIGHT_SHOT_FAIL;

    try
    {
        AiSnsMain* aisns = new AiSnsMain(*in_raw_format);

        *out_h = static_cast<void*>(aisns);
        *out_max_num_raws = 14;
    }
    catch (std::logic_error& e)
    {
        std::cerr << e.what() << std::endl;
        return AI_SUPER_NIGHT_SHOT_FAIL;
    }

    return AI_SUPER_NIGHT_SHOT_SUCCESS;
}

int AiSuperNightShotProcess(
    ai_super_night_shot_handle_t h, 
    const FrameInfo* in_frame,
    const ConfigInfo* in_anchor_idx,
    const size_t in_valid_len,
    uint16_t* out_frame)
{
    return AI_SUPER_NIGHT_SHOT_SUCCESS;
}

int AiSuperNightShotTerminate(ai_super_night_shot_handle_t h)
{
    if (nullptr==h)
        return AI_SUPER_NIGHT_SHOT_FAIL;

    AiSnsMain* aisns = static_cast<AiSnsMain*>(h);

    delete aisns;

    return AI_SUPER_NIGHT_SHOT_SUCCESS;
}

int AiSuperNightShotVersionInfo(int* out_main, int* out_major, int* out_minor)
{
    if(nullptr==out_main || nullptr==out_major || nullptr==out_minor)
        return AI_SUPER_NIGHT_SHOT_FAIL;

    *out_main = 0;
    *out_major = 0;
    *out_minor = 1;

    return AI_SUPER_NIGHT_SHOT_SUCCESS;
}

int main()
{
    return 0;
}
