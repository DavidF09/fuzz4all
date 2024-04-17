# Fuzz4All: Universal Fuzzing with Large Language Models

The following is the documentation for building and running a docker image to reproduce the paper's results.

## Building the docker image

Build the image that will be used to run a docker container.

```bash
docker build -t "IMAGE_NAME"

```

Note that `"IMAGE_NAME"` can be anything.

## Running the docker container

Now run the docker container.

```bash
docker run -it --rm "IMAGE_NAME"

```

You should be in the terminal of the docker container at this point.

## Setting up the fuzz4all environment

Enter the fuzz4all directory and use the fuzz4all conda environment.

```bash
cd fuzz4all
conda activate fuzz4all

```

Install the dependencies required for this artifact.

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
export GPT_MODEL="gpt-3.5-turbo"

```

Add this environment variable to be able to run the Fuzz4All process.

```bash
export OPENAI_API_KEY="KEY_HERE"

```

## Generate OpenAI API key

You will need to generate an OpenAI API key.

Click this [link](https://platform.openai.com/docs/quickstart?context=python) to find out more.

## Gain access to the code generation models

You will need to be granted access to the following models.

Click on [starcoderbase](https://huggingface.co/bigcode/starcoderbase) and [starcoderbase-1b](https://huggingface.co/bigcode/starcoderbase-1b) to do so.

## Login to the huggingface CLI

Eventually, you may need to login to the huggingface CLI to get access to the code generation models

```bash
huggingface-cli login

```

You may be prompted to enter a token. Click this [link](https://huggingface.co/docs/hub/security-tokens) to find out more.

Now you are ready to replicate the results from the paper.

## Reproducing the results

### Generate figures

This will produce the 6 figures in Figure 4 (in `fig/coverage-{target}.pdf`) using the coverage data collected in the runs.

```bash
rm -r fig/coverage-*
python tools/coverage/plot_full_run_coverage.py

```

You can download the figures by running the following command in your host machine:

```bash
docker cp <containerId>:fig .
```

### Generate table 2 data

This will render/output the table in Table 2 using coverage, validity and number of programs collected during the runs

```bash
python tools/coverage/draw_table.py

```

### Generate table 3 data

This will render/output the tables in Table 3 using both coverage and hit rate collected during the targeted runs

```bash
python tools/targeted/draw_table.py
```

### Generate table 4 data

This will render/output the table in Table 4 using both coverage and valid rate collected during the ablation runs

```bash
python tools/ablation/draw_table.py
```

### Generate table 2 on the web

This will generate an HTML file displaying Table 2 from the research paper.

```bash
python WebView/web_coverage.py

```

You can download the HTML file by running the following command in your host machine:

```bash
docker cp <containerId>:WebView/web_coverage.html .

```

### Generate table 3 on the web

This will generate an HTML file displaying Table 3 from the research paper.

```bash
python WebView/web_targeted.py

```

You can download the HTML file by running the following command in your host machine:

```bash
docker cp <containerId>:WebView/web_targeted.html .

```

### Generate table 4 on the web

This will generate an HTML file displaying Table 4 from the research paper.

```bash
python WebView/web_ablation.py

```

You can download the HTML file by running the following command in your host machine:

```bash
docker cp <containerId>:WebView/web_ablation.html .

```

### Generate figures on the web

This will generate an HTML file displaying the graphs from the research paper.

```bash
rm -r WebView/img/coverage-*
python WebView/web_full_coverage.py

```

You can download the HTML file and images by running the following command in your host machine:

```bash
docker cp <containerId>:WebView/web_full_coverage.html .
docker cp <containerId>:WebView/img .

```

### Generate fuzzing output and logs on the web

This will generate fuzzing outputs for the demo runs for cvc5 and g++.

```bash
flask --app WebView/app.py run

```

## Running the Fuzz4all fuzzer

### Enable permissions for the fuzz scripts.

Be sure to enable permissions for the scripts so you can be able to execute them.

```bash
chmod +x ./scripts/demo_run.sh
chmod +x ./scripts/full_run.sh
chmod +x ./scripts/ablation_run.sh
chmod +x ./scripts/targeted_run.sh
chmod +x ./scripts/build_cvc5_coverage.sh
chmod +x ./scripts/build_gcc_coverage.sh
chmod +x ./scripts/build_javac_coverage.sh
chmod +x ./scripts/build_qiskit_coverage.sh

```

### Run the fuzzing demo.

Below is start script to test whether the model is running smoothly.

```bash
./scripts/demo_run.sh

```

### Run the fuzzing full run.

You can run the full Fuzz4All process which includes auto-prompting + fuzzing.

```bash
./scripts/full_run.sh {target}

```

Note that `target` can be gcc, g++, go, javac, cvc5, or qiskit.
