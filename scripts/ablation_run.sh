#/bin/sh
target=$1

# check target is a valid target name:
if [ "$target" = "gcc" ]; then
    target_name="/home/gcc-13/bin/gcc"
    configs=("config/ablation/c_std_ap.yaml" "config/ablation/c_std_documentation.yaml" "config/ablation/c_std_no_input.yaml" "config/ablation/c_std_no_loop.yaml" "config/ablation/c_std_strategy.yaml")
elif [ "$target" = "g++" ]; then
    target_name="/home/gcc-13/bin/g++"
    configs=("config/ablation/cpp_23_ap.yaml" "config/ablation/cpp_23_documentation.yaml" "config/ablation/cpp_23_no_input.yaml" "config/ablation/cpp_23_no_loop.yaml" "config/ablation/cpp_23_strategy.yaml")
elif [ "$target" = "go" ]; then
    target_name="/home/go/bin/go"
    configs=("config/ablation/go_std_ap.yaml" "config/ablation/go_std_documentation.yaml" "config/ablation/go_std_no_input.yaml" "config/ablation/go_std_no_loop.yaml" "config/ablation/go_std_strategy.yaml")
elif [ "$target" = "javac" ]; then
    target_name="/home/javac/bin/javac"
    configs=("config/ablation/java_std_ap.yaml" "config/ablation/java_std_documentation.yaml" "config/ablation/java_std_no_input.yaml" "config/ablation/java_std_no_loop.yaml" "config/ablation/java_std_strategy.yaml")
elif [ "$target" = "cvc5" ]; then
    target_name="/home/cvc5/bin/cvc5"
    configs=("config/ablation/smt_general_ap.yaml" "config/ablation/smt_general_documentation.yaml" "config/ablation/smt_general_no_input.yaml" "config/ablation/smt_general_no_loop.yaml" "config/ablation/smt_general_strategy.yaml")
elif [ "$target" = "qiskit" ]; then
    target_name="python" # just python is enough.
    configs=("config/ablation/qiskit_ap.yaml" "config/ablation/qiskit_documentation.yaml" "config/ablation/qiskit_no_input.yaml" "config/ablation/qiskit_no_loop.yaml" "config/ablation/qiskit_strategy.yaml")
else
    echo "Invalid target name: $target"
    exit 1
fi

BATCH_SIZE="${FUZZING_BATCH_SIZE:-30}"
MODEL_NAME="${FUZZING_MODEL:-"bigcode/starcoderbase"}"
DEVICE="${FUZZING_DEVICE:-"gpu"}"

echo "BATCH_SIZE: $BATCH_SIZE"
echo "MODEL_NAME: $MODEL_NAME"
echo "DEVICE: $DEVICE"

if [ "$DEVICE" = "gpu" ]; then
    for config in "${configs[@]}"
    do
      IFS='/' read -ra ADDR <<< "$config"
      IFS='.' read -ra name <<< "${ADDR[2]}"
      echo ${name[0]}
      python Fuzz4All/fuzz.py --config $config main_with_config \
                              --folder outputs/ablation/${name[0]}/ \
                              --batch_size $BATCH_SIZE \
                              --model_name $MODEL_NAME \
                              --target $target_name
    done
else
    for config in "${configs[@]}"
    do
      IFS='/' read -ra ADDR <<< "$config"
      IFS='.' read -ra name <<< "${ADDR[2]}"
      echo ${name[0]}
      python Fuzz4All/fuzz.py --config $config main_with_config \
                              --folder outputs/ablation/${name[0]}/ \
                              --batch_size $BATCH_SIZE \
                              --model_name $MODEL_NAME \
                              --cpu \
                              --target $target_name
    done
fi
