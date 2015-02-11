def get_string_type(s):
    string_type = ""

    if isinstance(s, bytes):
        string_type = "bytes"
    elif isinstance(s, str):
        string_type = "str"
    else:
        string_type = "neither"

    return string_type
