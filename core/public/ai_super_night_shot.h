#ifndef _AI_SUPER_NIGHT_SHOT_H_
#define _AI_SUPER_NIGHT_SHOT_H_

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

#define AI_SUPER_NIGHT_SHOT_SUCCESS                  (0x00000000)
#define AI_SUPER_NIGHT_SHOT_FAIL                     (0x00000001)

#define AI_SUPER_NIGHT_SHOT__RAW_COLOR_SEQ_BGGR      (0x000000AA)
#define AI_SUPER_NIGHT_SHOT__RAW_COLOR_SEQ_RGGB      (0x000000AB)
#define AI_SUPER_NIGHT_SHOT__RAW_COLOR_SEQ_GBRG      (0x000000AC)
#define AI_SUPER_NIGHT_SHOT__RAW_COLOR_SEQ_GRBG      (0x000000AD)

#define AI_SUPER_NIGHT_SHOT__RAW_BIN_MIPI            (0x000000BA)
#define AI_SUPER_NIGHT_SHOT__RAW_BIN_PACKED          (0x000000BB)
#define AI_SUPER_NIGHT_SHOT__RAW_BIN_PLAIN           (0x000000BC)

struct RawFormat
{
    int width; 
    int height;
    unsigned int binary_format;
    unsigned int color_seq;
    unsigned int bit_depth;
};

struct GyroInfo
{
    float x[32];
    float y[32];
    float z[32];
    long time_stamp[32];
    size_t valid_len;
};

struct SharpnessInfo
{
    unsigned int v;
    long time_stamp;
};

struct ExposureInfo
{
    float exp_time;     // in second
    int lux_index;
    float digital_gain; // 1.0x -> no gain
    long time_stamp;
};

struct RawInfo
{
    void* buf;
    long time_stamp;
};

struct FrameInfo
{
    RawInfo raw;
    GyroInfo gyro;
    SharpnessInfo sharpness;
    ExposureInfo exposure;
};

struct ConfigInfo
{
    unsigned int anchor_idx;
};

typedef void* ai_super_night_shot_handle_t;

int AiSuperNightShotInit(
    const RawFormat* in_raw_format,
    ai_super_night_shot_handle_t* h, 
    size_t* max_num_raws);

int AiSuperNightShotProcess(
    ai_super_night_shot_handle_t h, 
    const FrameInfo* in_frame,
    const ConfigInfo* anchor_idx,
    const size_t valid_len,
    uint16_t* output);

int AiSuperNightShotTerminate(ai_super_night_shot_handle_t h);

int AiSuperNightShotVersionInfo(int* out_main, int* out_major, int* out_minor);

#ifdef __cplusplus
}; //extern C
#endif

#endif //_AI_SUPER_NIGHT_SHOT_H_
