FROM continuumio/miniconda3

WORKDIR /home

COPY . /home/fuzz4all

RUN conda init bash
RUN conda create -n fuzz4all python=3.10
ENV PATH /opt/conda/envs/env/bin:$PATH
