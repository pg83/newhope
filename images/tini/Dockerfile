FROM antonsamokhvalov/newhope:min
RUN (/bin/upm pkg add @tini) && (/bin/upm pkg del dash-run tar-run upm-run)
ENTRYPOINT /bin/sh -l -c ". /etc/profile; exec runsvdir /etc/runit"
