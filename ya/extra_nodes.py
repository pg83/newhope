def iter_workspace():
    yield {
        'output': 'workspace',
        'inputs': ['package_dir', 'work_dir', 'install_dir', 'cache_dir', 'source_dir', 'release_upm'],
        'build': [],
    }

    yield {
        'output': 'install_dir',
        'inputs': [],
        'build': [
            'rm -rf "$PD" 2> /dev/null || true',
            'mkdir -p "$PD"',
        ],
    }

    yield {
        'output': 'work_dir',
        'inputs': [],
        'build': [
            'rm -rf "$WD" 2> /dev/null || true',
            'mkdir -p "$WD"',
        ],
    }

    yield {
        'output': 'package_dir',
        'inputs': [],
        'build': [
            'mkdir -p "$RD"',
        ],
    }

    yield {
        'output': 'cache_dir',
        'inputs': [],
        'build': [
            'rm -rf "$MD" 2> /dev/null || true',
            'mkdir -p "$MD"',
        ],
    }

    yield {
        'output': 'source_dir',
        'inputs': [],
        'build': [
            'mkdir -p "$SD"',
            '(rm -rf $SD/upm || true) 2> /dev/null'
        ],
    }

    yield {
        'output': 'release_upm',
        'inputs': ['source_dir'],
        'build': [
            '($UPM cmd release > $SD/upm.tmp) && chmod +x $SD/upm.tmp && $SD/upm.tmp help && mv $SD/upm.tmp $SD/upm',
        ],
    }
