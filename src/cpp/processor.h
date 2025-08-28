/*
Copy Right. The EHPCL Authors.
*/

#ifndef PROCESSOR_H
#define PROCESSOR_H

#include <string>

#include "task.h"

namespace processor {
    
typedef ProcessorAffinity_t ProcessorType_t;

const std::string ProcessorTypeNames[10] = {
    "CPU",
    "CPUBigCore",
    "CPULittleCore",
    "DataCopy",
    "DataCopyHTD",
    "DataCopyDTH",
    "PE",
    "GPU",
    "FPGA",
    "UNKNOWN",
};

enum ProcessorState_t {
    IDLE,
    BUSY_PREEMPTIVE,
    BUSY_NONPREEMPTIVE,
    DEAD
};

enum ProcessorPreemption_t {
    PREEMPTIVE,
    NONPREEMPTIVE,
    UNKNOWN
};

typedef unsigned int ProcessorIndex_t;

};

using namespace processor;

class Segment;
class Task;

namespace task {
    typedef unsigned char TaskRTPriority_t;
    typedef unsigned long long TimeStamp_t;
};

class Processor {

protected:
    ProcessorType_t processorType = CPU;
    ProcessorPreemption_t processorPreemption = ProcessorPreemption_t::PREEMPTIVE;
    ProcessorState_t processorState = IDLE;
    ProcessorIndex_t processorGlobalIndex = 0;
    ProcessorIndex_t processorInternalIndex = 0;

    Task * currentTask = nullptr;
    Segment * currentSegment = nullptr;

    SegmentLength_t executionVariation = 0;

    task::TaskRTPriority_t currentTaskPriority = 99;
    // Number of parallel running processors of this type.
    unsigned int parallelBurdern = 1;
    unsigned int speedupDeductFactor = 0;

public:
    Task * getCurrentTask() const {return currentTask;};
    Segment * getCurrentSegment() const {return currentSegment;};

    bool operator<(const Processor & other) const {
        return processorType < other.processorType;
    }

    ProcessorType_t queryProcessorType() const {return processorType;};
    ProcessorState_t queryProcessorState() const {return processorState;};
    ProcessorIndex_t queryProcessorInternalIndex() {return processorInternalIndex;};
    ProcessorIndex_t queryProcessorGlobalIndex() {return processorGlobalIndex;};
    std::string queryProcessorTypeName() const {return processor::ProcessorTypeNames[processorType];}

    task::TaskRTPriority_t queryProcessorCurrentTaskPriority() {return currentTaskPriority;}

    void setProcessorInternalIndex(ProcessorIndex_t processorInternalIndex)
        {this->processorInternalIndex = processorInternalIndex;}
    void setProcessorGlobalIndex(ProcessorIndex_t processorGlobalIndex)
        {this->processorGlobalIndex = processorGlobalIndex;}

    void setProcessorState(ProcessorState_t processorNewState)
        {processorState = processorNewState;};

    /**
     * @param varation percentage (0-100) of the execution time variation
     */
    void setExecutionVariation(SegmentLength_t varation)
        {executionVariation = varation;};

    void setParallelBurdern(unsigned int parallelBurdern)
        {this->parallelBurdern = parallelBurdern;};

    void setSpeedupDeductFactor(unsigned int speedupDeductFactor)
        {this->speedupDeductFactor = speedupDeductFactor;};

    /**
     * @brief Schedule (as a decision) the given task on this processor, taking account
     * the processor affinity and preemption property. Though the schedule command is only
     * called from the processor side, the task state is changed internally after the
     * schedule is called.
    */
    bool scheduleTask(Task & taskToSchedule, task::TimeStamp_t timeStamp);

    bool scheduleTaskSpecifiedSegment(Task & taskToSchedule, Segment * Segment, task::TimeStamp_t timeStamp);

    // Default constructor, create an empty processor.
    Processor() {};

    Processor(ProcessorType_t processorType, ProcessorPreemption_t ProcessorPreemption,
              ProcessorIndex_t processorGlobalIndex):
              processorType(processorType), processorPreemption(ProcessorPreemption),
              processorGlobalIndex(processorGlobalIndex) {};

    // Simulate the behavior: either execute the task or keep idle
    // Update the processor state if necessary
    bool workProcessor(task::TimeStamp_t timeStamp);

    bool resetProcessor();

};

#endif // processor.h
