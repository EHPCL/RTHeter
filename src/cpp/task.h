/*
Copy Right. The EHPCL Authors.
*/

#ifndef TASK_H
#define TASK_H

#include <vector>
#include <list>

#include "segment.h"
#include "affinity.h"
#include "processor.h"

namespace task {

enum TaskPreemption_t {
    PREEMPTIVE,
    NONPREEMPTIVE,
    UNKNOWN
};

enum TaskRTProperty_t {
    HARDRT,
    SOFTRT,
    NONERT, // Current simulator does not support none RT Task.
};

typedef unsigned int TaskIndex_t;

enum SSTaskState_t {
    SS_EXECUTING,
    SS_SUSPENSION,
    SS_READY,
};

enum TaskState_t {
    TASKS_EXECUTING, // deprecated, tasks can be inter-parallel
    TASKS_READY,
    TASKS_FINISHED,
    TASKS_MISSDDL,
    TASKS_UNKNOWN,
};

/*enum HeterSSTaskState_t {
    TASKS_EXECUTING,
    TASKS_FINISHED,
    TASKS_READY,
    TASKS_MISSDDL,
    TASKS_UNKNOWN,
};*/

typedef unsigned long long TimeStamp_t;

typedef unsigned char TaskRTPriority_t;

// The value is same as "SCHED_***" defined in <sched.h>
enum TaskRTSchedulePolicy_t {
    HETER_SCHED_OTHER,
    HETER_SCHED_FIFO,
    HETER_SCHED_RR,
    HETER_SCHED_BATCH,
    HETER_SCHED_ISO,
    HETER_SCHED_IDLE,
    HETER_SCHED_DEADLINE,
};

};

using namespace task;


class Processor;

/**
 * @brief Class on task, can inherit to SSTask or DAGTask.
*/
class Task {

protected:

    // Internal storage, the instances of segments
    std::vector<Segment> segments = {};
    std::vector<std::list<SegmentIndex_t>> precedingSegments = {};
    std::vector<std::list<SegmentIndex_t>> successiveSegments = {};

    // Internal fixed properties
    SegmentLength_t segmentExecutionTime = 0;
    TaskRTProperty_t taskRealTimeProperty = TaskRTProperty_t::HARDRT;
    TaskIndex_t taskIndex;
    unsigned int maxParallism = 1;

    // Scheduling related properties
    TimeStamp_t taskRelativeDeadline = 0;
    TimeStamp_t taskAbsoluteDeadline = 0;
    TimeStamp_t taskExecutionTime = 0;

    TimeStamp_t taskPeriod = 0;
    TaskRTPriority_t taskPriority = 99;
    TaskRTSchedulePolicy_t taskSchedulePolicy = HETER_SCHED_FIFO;

    // Runtime maintainance (storage)
    TaskState_t taskState = TaskState_t::TASKS_UNKNOWN;
    SegmentLength_t executedLength = 0;
   
    bool processorMaskEnabled = false;
    std::vector<unsigned int> processorMasks = {};

    bool taskCompleted = false;

    std::vector<SegmentState_t> segmentStates;
    std::vector<SegmentIndex_t> readySegments = {};

public:

    Segment & createNewSegment(ProcessorAffinity_t processorAffinity, SegmentLength_t segmentLength);

    /**
     * @brief Initialize the internal task vector by a given vector.
     * @return False if the format is not correct, otherwise true.
     * @example Input segments: Type = {CPU,GPU}, segments = {3,1,2,4,5} -> C-G-C-G-C.
     * @attention Current version requires the processorTypes to be different.
    */
    bool initializeTaskByVector(std::vector<ProcessorAffinity_t> & processorType,
                                std::vector<SegmentLength_t> & segments);

    TimeStamp_t queryTaskPeriod() {return taskPeriod;}
    TimeStamp_t queryTaskRelativeDeadline() {return taskRelativeDeadline;}
    TaskRTPriority_t queryTaskRTPriority() {return taskPriority;}
    void setTaskPeriod(TimeStamp_t taskPeriod) {this->taskPeriod = taskPeriod;};
    void setTaskRelativeDeadline(TimeStamp_t deadline) {this->taskRelativeDeadline = deadline;};
    void setTaskRTPriority(TaskRTPriority_t priority) {this->taskPriority = priority;};

    void setTaskIndex(TaskIndex_t index);
    TaskIndex_t queryTaskIndex() {return taskIndex;}

    double queryTaskUtilization();
    double querySingleTaskUtilization(ProcessorAffinity_t processorAffinity);

    bool releaseTask(TimeStamp_t currentTime);
    
    TaskState_t checkTaskStates();
    TaskState_t queryTaskState() {return taskState;}
    SegmentLength_t queryExecutedSegLength() {return executedLength;}
    void setTaskState(TaskState_t state) {taskState = state;}
    
    bool isAllSegmentsCompleted();
    bool isTaskCompleted() {return isAllSegmentsCompleted();}
    
    // true if miss
    bool checkWhetherMissDDL(TimeStamp_t currentTime);

    unsigned int querySegmentCount() {return segments.size();};
    SegmentLength_t querySegmentExecutionTime() const;

    // TODO: improve task status printing
    friend std::ostream & operator<<(std::ostream & os, const Task & task) {
        os << std::string("Task ") << std::to_string(task.taskIndex);
        os << std::string(", period ") << std::to_string(task.taskPeriod);
        os << std::string(", state: ");
        switch (task.taskState) {
            case TASKS_EXECUTING:
                os << std::string("executing");break;
            case TASKS_FINISHED:
                os << std::string("finished");break;
            case TASKS_READY:
                os << std::string("ready");break;
            case TASKS_MISSDDL:
                os << std::string("missddl");break;
            default:
                os << std::string("unknown");break;
        }
        os << std::string(", prog: ") << std::to_string(task.executedLength) 
           << std::string("/") << std::to_string(task.querySegmentExecutionTime());
        return os;
    }

    bool isSegmentReady(SegmentIndex_t segmentIndex);
    /**
     * @brief Execute the given segment by 1 unit, need to take the preemption into account.
     * @return True if segment is succuessfully executed, otherwise false.
    */
    bool executeSegment(SegmentIndex_t segmentIndex, TimeStamp_t timeStamp);
    bool executeFirstReadySegment(TimeStamp_t timeStamp);

    bool resetTask(bool enforce = false);

    // Default constructor: create an empty task
    Task() {segments.reserve(10);};
    Task(TaskRTPriority_t taskPriority, TimeStamp_t taskPeriod):
    taskPriority(taskPriority), taskPeriod(taskPeriod), taskRealTimeProperty(HARDRT)
    {segments.reserve(10);};

    void setProcessorMasks(std::vector<unsigned int> & processorMasks)
        {this->processorMasks = processorMasks;};
    bool isProcessorMaskEnabled() {return processorMaskEnabled;};
    bool isInsideProcessorMasks(unsigned int processorGlobalIndex);

    TaskRTProperty_t queryTaskRTProperty() {return taskRealTimeProperty;};

    bool setTaskScheduled();
    // consider changes on heter ss task
    bool setTaskPreempted();
    void setFirstSegmentReady() {segments[0].markSegmentReady();}

    /**
     * @brief Configure dependency: seg2 depends on seg1
    */
    void setSegmentDependency(SegmentIndex_t seg1, SegmentIndex_t seg2);
    std::vector<SegmentIndex_t> & getReadySegments();
    std::vector<SegmentIndex_t> & queryReadySegments() {return readySegments;}
    Segment * getFirstReadySegment();
    Segment * getFirstReadySegment(ProcessorAffinity_t processorAffinity);
    Segment & getSegment(SegmentIndex_t segmentIndex) {return segments[segmentIndex];}

    bool setMaxParallism(int parallism) {
        if (parallism> this->maxParallism) this->maxParallism = parallism;
        else return false;
        return true;
    }

    void initStorage(int buffersize = 10);
};

class SSTask : public Task {

    SSTaskState_t SSTaskState;
    SegmentIndex_t currentSegmentIndex;

public:
    // Override the base class method, update the task state and current index.
    bool executeSegment(SegmentIndex_t SegmentIndex) {return true;};
    SSTaskState_t querySSTaskState() {return SSTaskState;};
    Segment & getCurrentSegment() {return segments[currentSegmentIndex];};
};

class DAGTask : public Task {

    // TODO

};

#endif // task.h
