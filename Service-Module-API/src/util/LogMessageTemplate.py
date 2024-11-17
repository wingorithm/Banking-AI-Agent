from enum import Enum

class LogMessageTemplate(Enum):
    """
    req = request_payload
    res = response_data / entity
    f = function_name
    s = step name
    p = path name /payload / parameters
    e = exception
    q = query_description
    """
    ROUTE_REQUEST = "REQUESTING | {p} with payload: {req}"
    ROUTE_RESPONSE = "RESPONSE | {p} for payload: {req}, response: {res}"
    SERVICE_START = "START SERVICE | {f} for {p}"
    SERVICE_PROGRESS = "PROGRESS SERVICE | {f} on step {s} for {p}"
    SERVICE_COMPLETE = "COMPLETE SERVICE | {f} for: {p}"
    SERVICE_ERROR = "ERROR SERVICE | {f} for: {p} knowing : {e}"
    REPO_START = "EXECUTING QUERY | {q} with parameters: {p}"
    REPO_COMPLETE = "QUERY RESULT | {q}: {res}"