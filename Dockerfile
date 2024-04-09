FROM continuumio/miniconda3

RUN conda init bash
RUN conda create -n fuzz4all python=3.10
ENV PATH /opt/conda/envs/env/bin:$PATH

RUN export FUZZING_BATCH_SIZE=5
RUN export FUZZING_MODEL="bigcode/starcoderbase-1b"
RUN export FUZZING_DEVICE="cpu"
RUN export OPENAI_API_KEY="KEY HERE"

WORKDIR /home/

RUN git clone https://github.com/DavidF09/fuzz4all.git
