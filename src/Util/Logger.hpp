#ifndef LOGGER_HPP
#define LOGGER_HPP

#include <iostream>
#include <fstream>
#include <string>
#include <ctime>
#include <sstream>

enum class LogLevel {
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    UNKNOWN
};

class Logger {
private:
    std::ofstream logFile;

    std::string getCurrentTime();
    std::string getStatusString(LogLevel status);
    std::string getCallingFile();
    std::string formatLogMessage(LogLevel status, const std::string& message);

public:
    Logger(const std::string& filename);
    ~Logger();
    void log(LogLevel status, const std::string& message);
};

#endif
