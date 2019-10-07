FROM antonsamokhvalov/newhope:latest
COPY Makefile consume produce fetch_file helper /runtime/
RUN (apk add curl wget) && mkdir /workdir && mkdir /repo && cd /repo && (PATH=/runtime:$PATH make -j 4 -f /runtime/Makefile all) && rm -rf /workdir /runtime
ENTRYPOINT ["bash", "-l"]
