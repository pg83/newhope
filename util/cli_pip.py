import re
import sys

from pip._internal import main


def cli_pip(args):
    sys.argv = ['pip3'] + args
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
