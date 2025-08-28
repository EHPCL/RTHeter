/*
Copy Right. The EHPCL Authors.
*/

#include "task.h"

bool Task::isSegmentReady(SegmentIndex_t segment) {
    if (segments[segment].isSegmentMarkedReady()) return true;
    for (SegmentIndex_t & segInd: precedingSegments[segment]) {
        if (!segments[segInd].isSegmentCompleted()) return false;
    }
    segments[segment].markSegmentReady();
    return true;
}

/**
 * @brief check the task state and update internal storage.
 * @attention different from querying, will detail examine each segments
*/
TaskState_t Task::checkTaskStates() {
    readySegments.clear();
    readySegments.reserve(segments.size());
    TaskState_t res = TASKS_UNKNOWN;
    
    executedLength = 0;
    for (SegmentIndex_t i = 0; i < segments.size(); i++) {
        executedLength += segments[i].querySegmentLength() - segments[i].querySegmentRemainLength();
        if (!segments[i].isSegmentCompleted()) {
            if (isSegmentReady(i)) {
                res = TASKS_READY;
                readySegments.push_back(i);
            }
        }
    }
    if (executedLength == querySegmentExecutionTime()) res = TASKS_FINISHED;
    taskState = res;
    return res;
}

void Task::setTaskIndex(TaskIndex_t index) {
    this->taskIndex = index;
}

Segment & Task::createNewSegment(ProcessorAffinity_t processorAffinity, SegmentLength_t segmentLength) {
    if (processorAffinity==CPU || processorAffinity==CPUBigCore || processorAffinity==CPULittleCore)
        this->segments.push_back(Segment(segmentLength, processorAffinity, SegmentPreemption_t::PREEMPTIVE));
    else
        this->segments.push_back(Segment(segmentLength, processorAffinity, SegmentPreemption_t::NONPREEMPTIVE));
    segments.back().setSegmentIndex(segments.size()-1);
    this->segmentExecutionTime += segmentLength;
    return segments.back();
}

bool Task::initializeTaskByVector(std::vector<ProcessorAffinity_t> & processorType,
                                  std::vector<SegmentLength_t> & segments) {
    this->segments.clear();
    this->segments.reserve(segments.size());

    // Insert segments into the tasks
    // Configure the dependencies
    unsigned int processorTypeCount = processorType.size();
    for (SegmentIndex_t i = 0; i < segments.size(); i++) {
        unsigned int processorTypeIndex = i%processorTypeCount;
        ProcessorAffinity_t type = processorType[processorTypeIndex];
        createNewSegment(type, segments[i]);
        if (i!=0) setSegmentDependency(i-1, i);
    }
    // self-suspension model, parallism = 1
    maxParallism = 1;
    segmentExecutionTime = querySegmentExecutionTime();
    return true;
}


SegmentLength_t Task::querySegmentExecutionTime() const {
    SegmentLength_t totalSegmentLength = 0;
    for (auto seg : segments)
        totalSegmentLength += seg.querySegmentLength();
    return totalSegmentLength;
}

double Task::queryTaskUtilization() {
    return querySegmentExecutionTime() / double(taskPeriod);
}

double Task::querySingleTaskUtilization(ProcessorAffinity_t processorAffinity) {
    SegmentLength_t totalSegmentLength = 0;
    for (Segment & seg : segments)
        if (seg.querySegmentProcessorAffinity()==processorAffinity)
            totalSegmentLength += seg.querySegmentLength();
    return totalSegmentLength / double(taskPeriod);
}


bool Task::releaseTask(TimeStamp_t currentTime) {
    if (!resetTask()) return false;
    
    setFirstSegmentReady();
    taskAbsoluteDeadline = taskPeriod + currentTime;
    this->taskState = TaskState_t::TASKS_READY;
    return true;
}


bool Task::checkWhetherMissDDL(TimeStamp_t currentTime) {
    if (taskState == TASKS_FINISHED) return false;
    bool res = (currentTime > taskAbsoluteDeadline);
    if (res) taskState = TASKS_MISSDDL;
    res = (currentTime + (segmentExecutionTime - executedLength)/maxParallism > taskAbsoluteDeadline);
    if (res) taskState = TASKS_MISSDDL;
    return res;
}


bool Task::isAllSegmentsCompleted() {
    for (Segment & seg : segments)
        if (!seg.isSegmentCompleted()) return false;
    return true;
}

bool Task::executeSegment(SegmentIndex_t segmentIndex, TimeStamp_t timeStamp) {
    bool res = segments[segmentIndex].executeSegment(timeStamp);
    if (!res) return false;
    if (segments[segmentIndex].isSegmentCompleted()) {
        for (SegmentIndex_t & segInd: successiveSegments[segmentIndex]) {
            isSegmentReady(segInd);
        }
        segments[segmentIndex].setCurrentProcessorIndex(999999);
    }
    return res;
}

bool Task::executeFirstReadySegment(TimeStamp_t timeStamp) {
    for (SegmentIndex_t i = 0; i < segments.size(); i++)
        if (isSegmentReady(i))
            return segments[i].executeSegment(timeStamp);
    return false;
}


bool Task::resetTask(bool enforce) {
    executedLength = 0;
    for (Segment & seg : segments)
       if (!seg.resetSegment(enforce)) return false;
    return true;
}

bool Task::isInsideProcessorMasks(processor::ProcessorIndex_t processorGlobalIndex) {
    for (ProcessorIndex_t index : processorMasks)
        if (processorGlobalIndex == index)
            return true;
    return false;
}

void Task::setSegmentDependency(SegmentIndex_t segment1, SegmentIndex_t segment2) {
    precedingSegments[segment2].push_front(segment1);
    successiveSegments[segment1].push_front(segment2);
    if (successiveSegments[segment1].size() > maxParallism)
        maxParallism = successiveSegments[segment1].size();
}

bool Task::setTaskScheduled() {
    setTaskState(TaskState_t::TASKS_EXECUTING);
    return true;
}

bool Task::setTaskPreempted() {
    setTaskState(TaskState_t::TASKS_READY);
    return true;
}

std::vector<SegmentIndex_t> & Task::getReadySegments() {
    readySegments.clear();
    for (SegmentIndex_t i = 0; i < segments.size(); i++)
        if (segments[i].querySegmentRemainLength()!=0 && isSegmentReady(i)) readySegments.push_back(i);
    return readySegments;
}

Segment * Task::getFirstReadySegment() {
    getReadySegments();
    for (SegmentIndex_t & i : readySegments)
        //if (segments[i].queryCurrentProcessorIndex() == 999999)
        return &(segments[i]);
    return nullptr;
}

Segment * Task::getFirstReadySegment(ProcessorAffinity_t processorAffinity) {
    getReadySegments();
    for (SegmentIndex_t & i : readySegments)
        if (segments[i].querySegmentProcessorAffinity()==processorAffinity)
            if (segments[i].queryCurrentProcessorIndex() == 999999)
                return &(segments[i]);
    return nullptr;
}

void Task::initStorage(int buffersize) {
    precedingSegments.resize(buffersize);
    successiveSegments.resize(buffersize);
    for (auto & seg: precedingSegments) seg.clear();
    for (auto & seg: successiveSegments) seg.clear();
}