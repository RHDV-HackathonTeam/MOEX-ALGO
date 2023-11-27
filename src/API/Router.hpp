#pragma once
#include <cpprest/http_listener.h>
#include <cpprest/json.h>

using namespace web;
using namespace web::http;

class Router {
   public:
    void handle_get(http_request request);
    void handle_post(http_request request);
    void handle_put(http_request request);
    void handle_delete(http_request request);
};