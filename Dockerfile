FROM continuumio/miniconda3

WORKDIR /home

COPY ./config ./fuzz4all/config
COPY ./Fuzz4All ./fuzz4all/Fuzz4All
COPY ./IntermediateResults ./fuzz4all/IntermediateResults
COPY ./scripts ./fuzz4all/scripts
COPY ./tools ./fuzz4all/tools
COPY ./WebView ./fuzz4all/WebView
COPY __init__.py ./fuzz4all
COPY requirements.txt ./fuzz4all
COPY setup.py ./fuzz4all

RUN conda init bash
RUN conda create -n fuzz4all python=3.10
ENV PATH /opt/conda/envs/env/bin:$PATH
