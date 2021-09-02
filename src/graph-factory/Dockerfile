FROM ubuntu:20.04

USER root

SHELL ["/bin/bash", "-c"]

ENV BASH_ENV=~/.bashrc                                          \
    MAMBA_ROOT_PREFIX=/srv/conda                                \
    PATH=/srv/conda/envs/env_graph_factory/bin:/srv/conda/envs/env_graph_factory/snap/bin:$PATH

ADD environment.yml /tmp/environment.yml

COPY . /tmp

# Install basic commands and mamba
RUN apt-get update && \
    apt-get install -y ca-certificates wget ttf-dejavu file bash bzip2  && \
    wget -qO- https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj bin/micromamba --strip-components=1 && \
    ./micromamba shell init -s bash -p ~/micromamba  && \
    apt-get clean autoremove --yes  && \
    rm -rf /var/lib/{apt,dpkg,cache,log}  && \
    cp ./micromamba /usr/bin  && \
    micromamba create -f /tmp/environment.yml 

RUN cd /tmp  && \
    /srv/conda/envs/env_graph_factory/bin/python setup.py install  && \
     rm -fr /srv/conda/pkgs  && \
     rm -fr /tmp/*

ADD snap.properties /srv/conda/envs/env_graph_factory/snap/etc/snap.properties
