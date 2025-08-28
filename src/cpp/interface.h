/*
Copy Right. The EHPCL Authors.
*/

#ifndef INTERFACE_H
#define INTERFACE_H

#include <unordered_map>
#include <functional>
#include "simulator.h"

class Interface {

    Simulator simulator;

    std::string tempOutput;

    std::unordered_map<std::string, std::function<std::string(const std::string&)>>
        command_map;

    bool quitFlag = false;

    bool interactive = false;

public:

    bool readCommands();

    std::string processCommand(const std::string & command);

    Simulator & getSimulator() {return simulator;};

    Interface();

    Interface(int argc, char ** argv);

    void initCommandMap();

    ProcessorAffinity_t stringtoProcessorAffinity(const std::string & processorAffinity);

    std::string startSimulation();

    std::string createProcessor(const std::string & args);

    std::string createDAGTask(const std::string & args);

    std::string createNewHeterSSTask(const std::string & args);

    std::string createEmptyTasks(const std::string & args);

    std::string setSimulationTimeBound(const std::string & args);

    std::string setProcessorVariation(const std::string & args);

    std::string setProcessorParallelFactor(const std::string & args);

    std::string queryProcessorStates();

    std::string queryProcessorState(const std::string & args);

    std::string segmentStateHelperFunc(unsigned int taskId, unsigned int segId);

    std::string queryTaskSpecifiedSegmentState(const std::string & args);

    std::string queryTaskSegmentStates(const std::string & args);

    std::string querySSTaskSegmentStates(const std::string & args);

    std::string querySSTaskStates(const std::string & args);

    std::string queryTaskExecutionStates();

    std::string queryTaskState(const std::string & args);

    std::string scheduleSegmentOnProcessor(const std::string & args);

    std::string updateProcessorAndTask();

    int parseFirstInteger(const std::string & args);

    std::string resetSimulator();

};

#endif // interface.h