/*
Copy Right. The EHPCL Authors.
*/

#include "processor.h"

bool Processor::scheduleTask(Task & taskToSchedule, task::TimeStamp_t timeStamp) {

    if (&(taskToSchedule) == currentTask) return true;
    if (currentTask) {
        // There's task going on the processor.
        // Check whether both processor and task support preemption
        if (processorPreemption!=ProcessorPreemption_t::PREEMPTIVE) return false;
        // currentTask->setTaskPreempted();
    }

    currentTask = &(taskToSchedule);
    // taskToSchedule.setTaskScheduled();
    processorState = BUSY_NONPREEMPTIVE;
    if (processorPreemption==ProcessorPreemption_t::PREEMPTIVE)
        processorState = BUSY_PREEMPTIVE;
    return true;
}

bool Processor::workProcessor(task::TimeStamp_t timeStamp) {
    if (processorState == IDLE) return true;
    if (!currentSegment->executeSegment(timeStamp, executionVariation, (parallelBurdern-1)*speedupDeductFactor)) return false;

    // TODO: Add temporal records here

    if (currentSegment->querySegmentRemainLength()<=0) {
        processorState = IDLE;
        currentTask = nullptr;
        currentSegment = nullptr;
    }
    return true;
}

bool Processor::scheduleTaskSpecifiedSegment(Task & taskToschedule, Segment * segment,
                                            task::TimeStamp_t currentTime) {
    if (segment->querySegmentProcessorAffinity() != this->queryProcessorType())
        return false;
    if (!segment->isSegmentMarkedReady()) return false;
    if (currentSegment == segment) return true;
    if (currentSegment) {
        // There's task going on processor
        if (processorPreemption!=ProcessorPreemption_t::PREEMPTIVE) return false;
        if (segment->queryCurrentProcessorIndex()!=999999)
            return false;
        currentTask->setTaskPreempted();
        currentSegment->setCurrentProcessorIndex(999999);
    }

    currentTask = &taskToschedule;
    currentSegment = segment;
    taskToschedule.setTaskScheduled();
    segment->setCurrentProcessorIndex(this->processorGlobalIndex);
    processorState = BUSY_NONPREEMPTIVE;
    if (processorPreemption==ProcessorPreemption_t::PREEMPTIVE)
        processorState = BUSY_PREEMPTIVE;
    return true;
}

bool Processor::resetProcessor(){
    currentTask = nullptr;
    currentSegment = nullptr;
    processorState = IDLE;
    return true;
}
