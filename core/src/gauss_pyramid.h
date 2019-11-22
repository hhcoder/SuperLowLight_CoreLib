#include "../public/ai_super_night_shot.h"

#include "base.h"

class GaussianPyramid : public ProcModuleBase
{
public:
    GaussianPyramid(const RawFormat& in_raw_format, unsigned in_max_num_raws)
        : ProcModuleBase("GaussianPyramid")
    {}

protected:
    virtual void DumpImpl(std::string& in_output_directory) 
    {
        std::ofstream ofs(in_output_directory + "/" + name, std::ios::out | std::ios::binary);
    }
    
};


