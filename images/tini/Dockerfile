FROM scratch
COPY ./1/ ./
RUN (/bin/upm pkg add @tini) && (/bin/upm pkg del dash-run tar-run upm-run)
