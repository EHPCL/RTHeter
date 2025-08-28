#include "scheduler.h"
#include <fstream>
#include <iostream>
    
bool Scheduler::initializeSimulation() {

    // Test case: 2 CPUs + 2 GPUs

    // Step 1: Initilize processors and tasks

    simulator.createNewProcessors(CPU, 2);
    simulator.createNewProcessors(GPU, 2);
    // It is recommended to sort in case created in a wrong order
    simulator.sortProcessorsByType();

    std::ifstream input_file;
    std:: cout << "Reading taskset infomation...\n";
    for (int i = 0; i < 5; i++) {
        std::string filename = "../test/.taskset_prop/task";
        // TODO: support task num > 10
        filename = filename + (char)(i+48);
        filename = filename + ".txt";
        input_file.open(filename);
        int deadlines;
        input_file >> deadlines;
        std::vector<SegmentLength_t> segments(10);
        for (int j = 0; j < 2*5-1; j++){
            input_file >> segments[j];
        }
        std::vector<ProcessorAffinity_t> processorTypes = {ProcessorAffinity_t::CPU, ProcessorAffinity_t::GPU};
        Task & tmp = simulator.createNewHeterSSTaskWithVector(processorTypes, segments);
        tmp.setTaskRelativeDeadline(deadlines);
        tmp.setTaskPeriod(deadlines);
        tmp.setTaskRTPriority(99-i);
        input_file.close();
    }

    // Step 2: Start simulation
    simulator.setSimulationTimeBound(120);
    return true;
}

bool Scheduler::startScheduleLoop() {

    while (! simulator.isSimulationCompleted()) {

        if (!simulator.checkTaskRelease()) return false;

        // TODO: Make decisions here
        if (!makeScheduleDecisions())
            std::cerr << "Scheduling decisions are inproper!\n";

        simulator.printSimulatorStates();

        simulator.updateProcessorAndTask();
    }

    return (!simulator.doesTaskMissDeadline());

}

bool Scheduler::makeScheduleDecisions() {
    // Cureent Implementation: based on SCHED_FIFO

    simulator.sortTasksByPriority();

    // First round: check IDLE Processors
    for (ProcessorIndex_t j = 0; j < simulator.queryProcessorCount(); j++) {
        Processor & proc = simulator.getProcessor(j);
        if (proc.queryProcessorState()!=IDLE) continue;
        for (TaskIndex_t i = 0; i < simulator.queryTaskCount(); i++) {
            Segment * readySegmet = simulator.getTask(i).
                                    getFirstReadySegment(proc.queryProcessorType());
            if (!readySegmet) continue;
            proc.scheduleTaskSpecifiedSegment(simulator.getTask(i), readySegmet, simulator.queryCurrentTimeStamp());
            break;
        }
    }
    // Next round: check preemptive processors
    for (ProcessorIndex_t j = 0; j < simulator.queryProcessorCount(); j++) {
        Processor & proc = simulator.getProcessor(j);
        if (proc.queryProcessorState()!=BUSY_PREEMPTIVE) continue;
        for (TaskIndex_t i = 0; i < simulator.queryTaskCount(); i++) {
            Task & task = simulator.getTask(i);
            if (task.queryTaskRTPriority() <= 
                proc.getCurrentTask()->queryTaskRTPriority()) continue;
            Segment * readySegmet = task.getFirstReadySegment(proc.queryProcessorType());
            if (!readySegmet) continue;
            proc.scheduleTaskSpecifiedSegment(simulator.getTask(i), readySegmet, simulator.queryCurrentTimeStamp());
            break;
        }
    }

    return true;
}