#include "Logger.hpp"

std::string Logger::getCurrentTime() {
    std::time_t now = std::time(nullptr);
    char timestamp[64];
    std::strftime(timestamp, sizeof(timestamp), "[%Y-%m-%d %H:%M:%S] ", std::localtime(&now));
    return std::string(timestamp);
}

std::string Logger::getStatusString(LogLevel status) {
    switch (status) {
        case LogLevel::DEBUG:
            return "[DEBUG] ";
        case LogLevel::INFO:
            return "[INFO] ";
        case LogLevel::WARNING:
            return "[WARNING] ";
        case LogLevel::ERROR:
            return "[ERROR] ";
        default:
            return "[UNKNOWN] ";
    }
}

std::string Logger::getCallingFile() {
    return __FILE__;
}

std::string Logger::formatLogMessage(LogLevel status, const std::string& message) {
    std::ostringstream formattedMessage;
    formattedMessage << getCurrentTime() << getStatusString(status) << "[" << getCallingFile() << "] " << message;
    return formattedMessage.str();
}

Logger::Logger(const std::string& filename) {
    logFile.open(filename, std::ios::out | std::ios::app);
    if (!logFile.is_open()) {
        std::cerr << "Unable to open log file: " << filename << std::endl;
    }
}

Logger::~Logger() {
    if (logFile.is_open()) {
        logFile.close();
    }
}

void Logger::log(LogLevel status, const std::string& message) {
    if (logFile.is_open()) {
        logFile << formatLogMessage(status, message) << std::endl;
    } else {
        std::cerr << "Log file is not open." << std::endl;
    }
}
