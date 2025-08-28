/*
Copy Right. The EHPCL Authors.
*/

#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "simulator.h"

class Scheduler {

    Simulator simulator;

    TaskRTSchedulePolicy_t schedulePolicy = HETER_SCHED_FIFO;

public:
    // Main schedule loop
    bool startScheduleLoop();

    bool initializeSimulation();

    bool makeScheduleDecisions();

    Simulator & getSimulator() {return simulator;};
};

#endif // scheduler.h
