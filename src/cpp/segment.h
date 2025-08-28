/*
Copy Right. The EHPCL Authors.
*/

#ifndef SEGMENT_H
#define SEGMENT_H

#include <vector>

#include "affinity.h"

namespace segment {

#ifdef VARI_PROC
typedef double SegmentLength_t;
#else
typedef unsigned int SegmentLength_t;
#endif
typedef unsigned int SegmentIndex_t;

enum SegmentState_t {
    SEG_EXECUTING,
    SEG_READY,
    SEG_NOTREADY,
    SEG_FINISHED,
    SEG_UNKNWON
};

enum SegmentPreemption_t {
    PREEMPTIVE,
    NONPREEMPTIVE,
    UNKNOWN
};

typedef SegmentIndex_t ProcessorIndex_t;
typedef unsigned long long TimeStamp_t;

};

using namespace segment;

/**
 * @brief Describe a segment (SS Task Model) or node (DAG Task Model). 
*/
class Segment {
    SegmentPreemption_t segmentPreemption = SegmentPreemption_t::PREEMPTIVE;
    SegmentLength_t segmentLength = 0;
    SegmentLength_t segmentRemainLength = 0;
    // The segment index inside its task.
    SegmentIndex_t segmentIndex = 0;

    ProcessorAffinity_t segmentAffinity;
    ProcessorIndex_t currentProcessor = 999999;

    std::vector<TimeStamp_t> executedAt = {};

    // Local storage to speed up the system.
    // Set to true if the corresponding methods return true.
    bool segmentCompleted = false;
    bool segmentReady = false;
public:
    bool isSegmentCompleted() {return segmentRemainLength==0;};
    void markSegmentReady() {segmentReady = true;};
    bool isSegmentMarkedReady() {return segmentReady;}

    SegmentLength_t querySegmentLength() const {return segmentLength;};
    SegmentLength_t querySegmentRemainLength() {return segmentRemainLength;};
    ProcessorAffinity_t querySegmentProcessorAffinity() {return segmentAffinity;}
    SegmentIndex_t querySegmentIndex() {return segmentIndex;}
    void setSegmentIndex(SegmentIndex_t index) {segmentIndex = index;}
    // may return false if the non-preemptive segment is not executed continuously
    bool executeSegment(TimeStamp_t timeStamp, SegmentLength_t variation = 0,  unsigned int parallelDiscount = 0);

    // Default constructor: create an empty segment
    Segment() {};
    Segment(SegmentLength_t segmentLength, ProcessorAffinity_t processorAffinity):
            segmentLength(segmentLength), segmentAffinity(processorAffinity)
            {};
    Segment(SegmentLength_t segmentLength, ProcessorAffinity_t processorAffinity, 
            SegmentPreemption_t segmentPreemption):
            segmentLength(segmentLength), segmentAffinity(processorAffinity),
            segmentPreemption(segmentPreemption) {};
    
    /**
     * @brief Task may be periodic, the segment is reinited and executed again.
     * @return True if reseted successfully, False if the reset behavior is inproper,
     * e.g. reset before the segment has finished.
    */
    bool resetSegment(bool enforce = false);

    void setCurrentProcessorIndex(ProcessorIndex_t processorInd) 
        {currentProcessor = processorInd;};
    ProcessorIndex_t queryCurrentProcessorIndex() { return currentProcessor;};
};

#endif // segment.h