# Fuzz4All: Universal Fuzzing with Large Language Models

The following is the documentation for building and running a docker image to reproduce the paper's results.

## Build the docker image

We will need to build the image that will be used to run a docker container.

```bash
docker build -t "IMAGE_NAME"

```

Note that `"IMAGE_NAME"` can be anything.

## Running the docker container

Now we need to run the docker container.

```bash
docker run -it --rm "IMAGE_NAME"

```

You should be in the terminal of the docker container at this point.

## Setting up the fuzz4all environment

Go to the fuzz4all directory.

```bash
cd fuzz4all

```

Use the fuzz4all conda environment.

```bash
conda activate fuzz4all

```

Install any dependencies required for this artifact.

```bash
pip install -r requirements.txt
pip install -e .

```

(OPTIONAL) Add these environment variables if you don't have a strong computer.

```bash
export FUZZING_BATCH_SIZE=5
export FUZZING_MODEL="bigcode/starcoderbase-1b"
export FUZZING_DEVICE="cpu"

```

(OPTIONAL) Add this environment variable if you don't have access to GPT-4.

```bash
export OPENAI_API_KEY="KEY_HERE"

```

You will need to generate an OpenAI API key.

Click this [link](https://platform.openai.com/docs/quickstart?context=python) to find out more.

Eventually, you may need to login to the huggingface CLI to get access to the code generation models

```bash
huggingface-cli login

```

You may be prompted to enter a token. Click this [link](https://huggingface.co/docs/hub/security-tokens) to find out more.

Additionally, you will need to be granted access to the following models.

Click on [starcoderbase](https://huggingface.co/bigcode/starcoderbase) and [starcoderbase-1b](https://huggingface.co/bigcode/starcoderbase-1b) to do so.

Now you are ready to replicate the results from the paper.

## Reproducing the results
