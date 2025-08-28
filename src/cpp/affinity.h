/*
Copy Right. The EHPCL Authors.
*/

#ifndef AFFINITY_H
#define AFFINITY_H

/**
 * @brief Describes task affinity on which types of processors,. 
*/
enum ProcessorAffinity_t {
    CPU,
    CPUBigCore,
    CPULittleCore,
    DataCopy,
    DataCopyHTD,
    DataCopyDTH,
    PE,
    GPU,
    FPGA,
    UNKNOWN
};

#endif // affinity.h
