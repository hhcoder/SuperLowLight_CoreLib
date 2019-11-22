import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def ReadBayerRaw(src_fname, in_width, in_height):
    in_length = in_width * in_height
    raw_buffer = np.fromfile(src_fname, dtype=np.uint8, count=in_length*5)
    # in_raw_file_size = int(in_length * 10 / 8)
    bayer_raw = np.zeros(in_length)

    convert_len = int(in_length/4)
    for i in range(convert_len):
        v0 = int(raw_buffer[5*i])
        v1 = int(raw_buffer[5*i+1])
        v2 = int(raw_buffer[5*i+2])
        v3 = int(raw_buffer[5*i+3])
        v4 = int(raw_buffer[5*i+4])
        bayer_raw[4*i]= (v0 << 2) | (v4 & 0x03)
        bayer_raw[4*i+1]= (v1 << 2) | ((v4>>2) & 0x03)
        bayer_raw[4*i+2]= (v2 << 2) | ((v4>>4) & 0x03)
        bayer_raw[4*i+3]= (v3 << 2) | ((v4>>6) & 0x03)

    return np.reshape(bayer_raw, (in_height, in_width))

def Crop(bayer_raw, new_x, new_y, new_width, new_height):
    return bayer_raw[new_y:(new_y+new_height):1, new_x:(new_x+new_width):1]

def InterpolateGChannel(bayer_raw):
    (in_width,in_height) = bayer_raw.shape
    g_interleaved = bayer_raw

    g_interleaved[0:in_height:2, 1:in_width:2] = 0

    g_interleaved[2:in_height-2:2, 3:in_width-2:2] =  \
        (g_interleaved[1:in_height-3:2, 3:in_width-2:2] + 
        g_interleaved[3:in_height-1:2, 3:in_width-2:2] +
        g_interleaved[2:in_height-2:2, 2:in_width-3:2] +
        g_interleaved[2:in_height-2:2, 4:in_width-1:2]) / 4 

    g_interleaved[1:in_height:2, 0:in_width:2] = 0

    g_interleaved[3:in_height-2:2, 2:in_width-2:2] = \
        (g_interleaved[2:in_height-3:2, 2:in_width-2:2] +
        g_interleaved[4:in_height-1:2, 2:in_width-2:2] +
        g_interleaved[3:in_height-2:2, 1:in_width-3:2] +
        g_interleaved[3:in_height-2:2, 3:in_width-1:2]) / 4 

    return g_interleaved

def GetGChannel(src_fname, in_width, in_height, reference_frame_idx):
    
    g_channel = []

    for n in range(0, len(src_fname), 1):
        raw = ReadBayerRaw(src_fname[n], in_width, in_height) 
        bayer_raw = Crop(raw, 1800, 0, 20, 20)

        # plt.figure()
        # plt.imshow(bayer_raw, cmap='gray', interpolation='nearest')
        # plt.title('Original Bayer GRBG: ' + str(n))
        # plt.draw()
        # plt.show(block=False)

        g_channel.append( InterpolateGChannel(bayer_raw) )

        plt.figure()
        plt.imshow(g_channel[n], cmap='gray')
        plt.title('Interpolated G Channel : ' + str(n))
        plt.show(block=False)
    
    return g_channel

def SimpleBayerAverage(g_channel):
    simple_avg = np.zeros(g_channel[0].shape)
    for n in range(0, len(g_channel), 1):
        simple_avg += g_channel[n]
    simple_avg /= num_of_raws
    return simple_avg

from scipy import fftpack

def Dct2dForward(img):
    return fftpack.dct(fftpack.dct(img.T, norm='ortho').T, norm='ortho')

def Dct2dInverse(coefficients):
    return fftpack.idct(fftpack.idct(coefficients.T, norm='ortho').T, norm='ortho')

# TODO: analyze and enhace frequency domain 
def Divide(d, n):
    try:
        return d/n
    except ZeroDivisionError:
        return 1

def EnhanceDct(g_block_dct, ref_idx):
    (b_h, b_w) = g_block_dct[0].shape
    var_mask = np.zeros((b_h, b_w))
    for j in range(0,b_h,1):
        for i in range(0,b_w,1):
            var_list = []
            for n in range(0, len(g_block_dct), 1):
                var_list.append(g_block_dct[n][j, i])
            var_mask[j, i] = np.var(var_list)
    
    increase_ratio =  Divide(g_block_dct[ref_idx], g_block_dct[ref_idx] + var_mask)
    return g_block_dct[ref_idx] * increase_ratio

def HTBayerDenoise(g_channel):

    (proc_height, proc_width) = g_channel[0].shape 

    aggregated_result = np.zeros((proc_height, proc_width))

    even_x = range(0,proc_width,2)
    even_y = range(1,proc_height,2)

    for j in range(0,len(even_y),1):
        for i in range(0,len(even_x),1):
            g_block_dct = []
            for n in range(0, num_of_raws, 1):
                g_block = g_channel[n][even_y[j]:even_y[j]+8:1, even_x[i]:even_x[i]+8:1]
                g_block_dct.append( Dct2dForward(g_block) )
            g_block_dct_modified = EnhanceDct(g_block_dct, ref_idx)
            g_block_idct = Dct2dInverse(g_block_dct_modified)
            aggregated_result[even_y[j]:even_y[j]+8:1, even_x[i]:even_x[i]+8:1] += g_block_idct

    odd_x = range(0,proc_width,2)
    odd_y = range(1,proc_height,2)

    for j in range(0, len(odd_y), 1):
        for i in range(0, len(odd_x), 1):
            g_block_dct = []
            for n in range(0, num_of_raws, 1):
                g_block = g_channel[n][odd_y[j]:odd_y[j]+8:1, odd_x[i]:odd_x[i]+8:1]
                g_block_dct.append( Dct2dForward(g_block) )
            g_block_dct_modified = EnhanceDct(g_block_dct, ref_idx)
            g_block_idct = Dct2dInverse(g_block_dct_modified)
            aggregated_result[odd_y[j]:odd_y[j]+8:1, odd_x[i]:odd_x[i]+8:1] += g_block_idct

    aggregated_result /= ((8*8)/(2*2))

    return aggregated_result


# Read all these information from config file
src_fname = [ "./201709220634380r_4032x3024_157.raw",
            "./201709220634380r_4032x3024_157.raw", 
            # "./201709220634380r_4032x3024_157.raw", 
            # "./201709220634380r_4032x3024_157.raw", 
            # "./201709220634380r_4032x3024_157.raw", 
            # "./201709220634380r_4032x3024_157.raw", 
            # "./201709220634380r_4032x3024_157.raw", 
            "./201709220634380r_4032x3024_157.raw" ]
in_width = 4032
in_height = 100 
ref_idx = 0 # from pre-processing

g_channel = GetGChannel(src_fname, in_width, in_height, ref_idx)

num_of_raws = len(g_channel)

aggregated_result = HTBayerDenoise(g_channel)

plt.figure()
plt.imshow(aggregated_result, cmap='gray')
plt.title('Aggregated Result')
plt.show(block=False)

simple_avg = SimpleBayerAverage(g_channel)

plt.figure()
plt.imshow(simple_avg, cmap='gray')
plt.title('Simple Average Result')
plt.show(block=False)

plt.figure()
plt.show(block=True)
