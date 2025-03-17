def success_response(data=None, status=200, message="success"):
    return {"success": True, "data": data, "message": message}, status


def error_response(data=None, status=400, message="error"):
    return {"success": False, "data": data, "message": message}, status
