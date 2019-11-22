#pragma once

#include <string>
#include <fstream>
#include <vector>

class ProcModuleBase
{
public:
	static void EnableAllDump(const std::string& in_output_directory) 
    { 
        output_directory = in_output_directory;
        dump_enabled = true; 
    }

	static void DisableAllDump() { dump_enabled = false; }

private:
	static bool dump_enabled;
    static std::string output_directory;

protected:
	std::string name;
    virtual void DumpImpl(std::string& in_output_directory) = 0;

public:
	ProcModuleBase(const std::string& in_name)
		: name(in_name)
	{
	}

    void Dump() 
    {
        if (dump_enabled)
            DumpImpl(output_directory);
    }
};
