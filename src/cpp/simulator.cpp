/*
Copy Right. The EHPCL Authors.
*/

#include <algorithm>
#include <iostream>
#include <iomanip>

#include "simulator.h"

ProcessorPreemption_t Simulator::queryProcessorPreemptionBasedonType(ProcessorType_t processorType) {
    if (processorType==CPU) return ProcessorPreemption_t::PREEMPTIVE;
    if (processorType==CPUBigCore) return ProcessorPreemption_t::PREEMPTIVE;
    if (processorType==CPULittleCore) return ProcessorPreemption_t::PREEMPTIVE;
    return ProcessorPreemption_t::NONPREEMPTIVE;
}

bool Simulator::createNewProcessor(processor::ProcessorType_t processorType) {
    unsigned int currentProcessorNum = processors.size();
    ProcessorPreemption_t processorPreemption = queryProcessorPreemptionBasedonType(processorType);
    processors.push_back(Processor(processorType, processorPreemption, currentProcessorNum));
    return true;
}

bool Simulator::createNewProcessors(processor::ProcessorType_t processorType, 
                                    unsigned int processorCount) {
    for (unsigned int i = 0 ; i < processorCount; i++)
        if (!createNewProcessor(processorType)) return false;
    return true;
}

bool Simulator::updateParallelBurdern() {
    int lastIndex = 0;
    for (auto & typeCount: processorCountByType) {
        unsigned int burdern = 0;
        for (unsigned int i = lastIndex; i < lastIndex + typeCount; i++)
            if (processors[i].queryProcessorState() != ProcessorState_t::IDLE) burdern++;
        for (unsigned int i = lastIndex; i < lastIndex + typeCount; i++)
            processors[i].setParallelBurdern(burdern);
        lastIndex += typeCount;
    }
    return true;
}

bool Simulator::setProcessorParallelFactor(ProcessorAffinity_t processorType, unsigned int speedupDeductFactor) {
    for (unsigned int i = 0; i < processors.size(); i++) {
        if (processors[i].queryProcessorType() == processorType) {
            processors[i].setSpeedupDeductFactor(speedupDeductFactor);
        }
    }
    return true;
}

bool Simulator::sortProcessorsByType() {
    std::sort(processors.begin(), processors.end(), std::less<Processor>());
    for (unsigned int i = 0; i < processors.size(); i++)
        processors[i].setProcessorGlobalIndex(i);
    ProcessorAffinity_t lastType = ProcessorAffinity_t::UNKNOWN;
    unsigned int lastCount = 0;
    for (auto & processor : processors) {
        if (processor.queryProcessorType() != lastType) {
            if (lastCount > 0) processorCountByType.push_back(lastCount);
            lastCount = 1;
            lastType = processor.queryProcessorType();
        }
        processor.setProcessorInternalIndex(lastCount-1);
        lastCount++;
    }
    return true;
}

ProcessorState_t Simulator::queryProcessorState(ProcessorIndex_t processorGlobalIndex) {
    return processors[processorGlobalIndex].queryProcessorState();
}

TaskState_t Simulator::queryTaskState(TaskIndex_t taskIndex) {
    return taskset[taskIndex].queryTaskState();
}

Task & Simulator::createNewTask() {
    taskset.push_back(Task());
    taskset.back().initStorage();
    taskset.back().setTaskIndex(taskset.size()-1);
    return taskset.back();
}

Task & Simulator::createNewHeterSSTaskWithVector(std::vector<ProcessorAffinity_t> processorType,
                                                        std::vector<SegmentLength_t> segments) {
    Task & result = createNewTask();
    result.initializeTaskByVector(processorType, segments);
    return result;
}

bool Simulator::checkTaskRelease() {
    if (taskReleaseCheckedThisRound) return true;
    for (Task & task: taskset) {
        if (currentTimeStamp%task.queryTaskPeriod()==0) {
            if (!task.releaseTask(currentTimeStamp))
                return false;
        }
    }
    return (taskReleaseCheckedThisRound = true);
}

int Simulator::updateProcessorAndTask() {
    if (!taskReleaseCheckedThisRound) checkTaskRelease();

    updateParallelBurdern();

    for (Processor & processor: processors) {
        if (!processor.workProcessor(currentTimeStamp)) {
            std::cerr << "Processor " << processor.queryProcessorGlobalIndex() << " working error!\n";
        }
    }

    int temp = 0;

    currentTimeStamp++;
    
    for (Task & task: taskset) {
        task.checkTaskStates();
        if (task.checkWhetherMissDDL(currentTimeStamp))
            taskMissDeadline = true;
        temp += task.queryExecutedSegLength();
    }

    temp = temp - taskExecutedTotal;
    taskExecutedTotal += temp;
    
    taskReleaseCheckedThisRound = false;
    checkTaskRelease();
    if (taskExecutedTotal == 0 ) return 0;
    return temp;
}


void Simulator::initializeStorages() {
    taskset.reserve(10);
    processors.reserve(10);
}

Simulator::Simulator() {
    initializeStorages();
}

static std::ostream & operator<<(std::ostream & os, const Processor & processor) {
    os << std::string("State: ");
    switch (processor.queryProcessorState()) {
        case IDLE:
            os << std::string("idle");break;
        case BUSY_PREEMPTIVE:
            os << std::string("busy-preemptive");break;
        case BUSY_NONPREEMPTIVE:
            os << std::string("busy-nonpreemptive");break;
        case DEAD:
            os << std::string("dead");break;
        default:
            os << std::string("unknown");break;
    }
    os << std::string(", Task ");
    if (processor.getCurrentTask())
    os << std::to_string(processor.getCurrentTask()->queryTaskIndex());
    os << std::string(", Segment");
    if (processor.getCurrentSegment())
    os << std::string("(") << std::to_string(processor.getCurrentSegment()->querySegmentIndex()) << std::string("): ")
       << std::to_string(processor.getCurrentSegment()->querySegmentLength() - processor.getCurrentSegment()->querySegmentRemainLength())
       << std::string("/") << std::to_string(processor.getCurrentSegment()->querySegmentLength());
    return os;
}


void Simulator::printSimulatorStates() {
    std::cerr << "Current Timestamp: " << currentTimeStamp << std::endl;
    unsigned int count = 0;
    for (Task & task : taskset) {
        std::cerr <<  task << std::endl;
    }
    count = 0;
    for (Processor & processor: processors) {
        std::cerr << processor.queryProcessorTypeName();
        std::cerr << count++ << " " << processor << std::endl;
    }
    std::cerr << std::endl;
}

bool Simulator::resetSimulator() {
    this->currentTimeStamp = 0;
    taskMissDeadline = 0;
    for (Task & task: taskset)
        if (!task.resetTask(true)) return false;
    for (Processor & proc: processors)
        if (!proc.resetProcessor()) return false;
    return true;
    this->checkTaskRelease();
}
