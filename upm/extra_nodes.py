def iter_workspace():
    path = 'export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin'

    yield {
        'output': 'workspace',
        'inputs': ['$RD/x', '$WD/x', '$PD/x', '$MD/x', '$SD/x', '$SD/upm'],
        'build': [],
    }

    yield {
        'output': '$PD/x',
        'inputs': [],
        'build': [
            path,
            'rm -rf "$PD" 2> /dev/null || true',
            'mkdir -p "$PD"',
        ],
    }
    
    yield {
        'output': '$WD/x',
        'inputs': [],
        'build': [
            path,
            'rm -rf "$WD" 2> /dev/null || true',
            'mkdir -p "$WD"',
        ],
    }
    
    yield {
        'output': '$RD/x',
        'inputs': [],
        'build': [
            path,
            'mkdir -p "$RD"',
        ],
    }
    
    yield {
        'output': '$MD/x',
        'inputs': [],
        'build': [
            path,
            'mkdir -p "$MD"',
        ],
    }
    
    yield {
        'output': '$SD/x',
        'inputs': [],
        'build': [
            path,
            'mkdir -p "$SD"',
            '(rm -rf $SD/upm || true) 2> /dev/null'
        ],
    }
    
    yield {
        'output': '$SD/upm',
        'inputs': ['$SD/x'],
        'build': [
            path,
            '($UPM cmd release > $SD/upm.tmp) && chmod +x $SD/upm.tmp && $SD/upm.tmp help && mv $SD/upm.tmp $SD/upm',
        ],
    }
