FROM continuumio/miniconda3

WORKDIR /artifact/

RUN git clone https://github.com/DavidF09/fuzz4all.git

WORKDIR /artifact/fuzz4all

RUN git checkout -b create-dockerfile

RUN conda init bash
RUN conda env create -f environment.yml
ENV PATH /opt/conda/envs/env/bin:$PATH

RUN export FUZZING_BATCH_SIZE=5
RUN export FUZZING_MODEL="bigcode/starcoderbase-1b"
RUN export FUZZING_DEVICE="cpu"
RUN export OPENAI_API_KEY="KEY HERE"
