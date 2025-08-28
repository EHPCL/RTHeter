/*
Copy Right. The EHPCL Authors.
*/

#include <sys/time.h>

#include "segment.h"


bool Segment::resetSegment(bool enforce) {
    if (!enforce && segmentRemainLength !=0) return false;
    executedAt.clear();
    segmentRemainLength = segmentLength;
    currentProcessor = 999999;
    segmentCompleted = false;
    segmentReady = false;
    return true;
}

bool Segment::executeSegment(TimeStamp_t timeStamp, SegmentLength_t variation, unsigned int parallelDiscount) {
    if (segmentRemainLength<=0) return false;
    if (segmentPreemption==SegmentPreemption_t::NONPREEMPTIVE)
    if (!executedAt.empty() && executedAt.back()+1!=timeStamp) return false;
    struct timeval sys_time;
    gettimeofday(&sys_time, nullptr);
    segmentRemainLength -= (1.0 - parallelDiscount / 100.0) * (1.0 - variation / 100.0 * (sys_time.tv_usec%(int(variation+1))));
    executedAt.push_back(timeStamp);
    if (segmentRemainLength <= 0) {
        segmentRemainLength = 0;
        segmentCompleted = true;
        segmentReady = false;
    }
    return true;
}

