import os


@y.defer_constructor
def init():
    #@y.read_callback('orig functions', 'gt')
    #@y.read_callback('new functions', 'gt')
    #@y.read_callback('new plugin', 'gt')
    #@y.read_callback('new functions templates', 'gt')
    def cb(arg):
        print arg

    @y.read_callback('SIGINT', 'pg')
    def sigint(arg):
        print arg
        #os._exit(0)
