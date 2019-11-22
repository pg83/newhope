def iter_workspace():
    yield {
        'output': 'workspace',
        'inputs': ['$RD/x', '$WD/x', '$PD/x', '$MD/x'],
        'build': [],
    }

    yield {
        'output': '$PD/x',
        'inputs': [],
        'build': [
            'export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin',
            'rm -rf "$PD" 2> /dev/null || true',
            'mkdir -p "$PD"',
        ],
    }
    
    yield {
        'output': '$WD/x',
        'inputs': [],
        'build': [
            'export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin',
            'rm -rf "$WD" 2> /dev/null || true',
            'mkdir -p "$WD"',
        ],
    }
    
    yield {
        'output': '$RD/x',
        'inputs': [],
        'build': [
            'export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin',
            'mkdir -p "$RD"',
        ],
    }
    
    yield {
        'output': '$MD/x',
        'inputs': [],
        'build': [
            'export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin',
            'mkdir -p "$MD"',
        ],
    }
