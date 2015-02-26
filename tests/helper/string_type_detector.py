def get_string_type(unknown_string) -> str:
    if isinstance(unknown_string, bytes):
        string_type = 'bytes'
    elif isinstance(unknown_string, str):
        string_type = 'str'
    else:
        string_type = 'neither'

    return string_type
