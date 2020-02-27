#!/bin/sh

exec docker run -ti --mount type=bind,src=/,dst=/srv $@ /bin/sh -l
