#/bin/sh
target=$1

# check target is a valid target name:
if [ "$target" = "gcc" ]; then
    target_name="/home/gcc-13/bin/gcc"
    config="config/full_run/c_std.yaml"
elif [ "$target" = "g++" ]; then
    target_name="/home/gcc-13/bin/g++"
    config="config/full_run/cpp_23.yaml"
elif [ "$target" = "go" ]; then
    target_name="/home/go/bin/go"
    config="config/full_run/go_std.yaml"
elif [ "$target" = "javac" ]; then
    target_name="/home/javac/bin/javac"
    config="config/full_run/java_std.yaml"
elif [ "$target" = "cvc5" ]; then
    target_name="/home/cvc5/bin/cvc5"
    config="config/full_run/smt_general.yaml"
elif [ "$target" = "qiskit" ]; then
    target_name="python" # just python is enough.
    config="config/full_run/qiskit_opt_and_qasm.yaml"
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
    python Fuzz4All/fuzz.py --config $config main_with_config \
                            --folder outputs/full_run/$target/ \
                            --batch_size $BATCH_SIZE \
                            --model_name $MODEL_NAME \
                            --target $target_name
else
    python Fuzz4All/fuzz.py --config $config main_with_config \
                            --folder outputs/full_run/$target/ \
                            --batch_size $BATCH_SIZE \
                            --model_name $MODEL_NAME \
                            --cpu \
                            --target $target_name
fi
