#/bin/sh
target=$1

# check target is a valid target name:
if [ "$target" = "gcc" ]; then
    target_name="/home/gcc-13/bin/gcc"
    configs=("config/targeted/c_goto.yaml" "config/targeted/c_typedef.yaml" "config/targeted/c_union.yaml")
elif [ "$target" = "g++" ]; then
    target_name="/home/gcc-13/bin/g++"
    configs=("config/targeted/cpp_apply.yaml" "config/targeted/cpp_expected.yaml" "config/targeted/cpp_variant.yaml")
elif [ "$target" = "go" ]; then
    target_name="/home/go/bin/go"
    configs=("config/targeted/go_atomic.yaml" "config/targeted/go_big.yaml" "config/targeted/go_heap.yaml")
elif [ "$target" = "javac" ]; then
    target_name="/home/javac/bin/javac"
    configs=("config/targeted/java_finally.yaml" "config/targeted/java_instanceof.yaml" "config/targeted/java_synchronize.yaml")
elif [ "$target" = "cvc5" ]; then
    target_name="/home/cvc5/bin/cvc5"
    configs=("config/targeted/smt_arrays.yaml" "config/targeted/smt_bitvectors.yaml" "config/targeted/smt_real.yaml")
elif [ "$target" = "qiskit" ]; then
    target_name="python"
    configs=("config/targeted/qiskit_for_loop.yaml" "config/targeted/qiskit_linear_function.yaml" "config/targeted/qiskit_switch.yaml")
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
                              --folder outputs/targeted/${name[0]}/ \
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
                              --folder outputs/targeted/${name[0]}/ \
                              --batch_size $BATCH_SIZE \
                              --model_name $MODEL_NAME \
                              --cpu \
                              --target $target_name
    done
fi
