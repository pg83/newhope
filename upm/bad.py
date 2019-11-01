@y.singleton
def bad_substring():
    BAD_SUBSTRINGS = [
        'command not found',
        'Error:',
        '***',
        'C compiler cannot create executables',
        'No such file or directory',
        'Error is not recoverable: exiting now',
        'Error opening archive: Failed to open',
        'Traceback',
        'File format not recognized'
        'Broken pipe',
    ]

    return BAD_SUBSTRINGS
