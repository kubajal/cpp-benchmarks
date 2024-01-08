
set -x
set -e

if [ ! -d nested ] ; then

    mkdir nested nested_templated tuple

    echo "Generating cpp files"
    python main.py

    echo "Compiling C++ files"
    find tuple/*.cpp | xargs -I{} g++ {} -o {}.out
    find nested/*.cpp | xargs -I{} g++ {} -o {}.out
    find nested_templated/*.cpp | xargs -I{} g++ {} -o {}.out
fi

echo "Executing measurements"
output_csv="out.csv"
rm -f "$output_csv"
for dir in "nested" "nested_templated" "tuple"; do
    for file in $dir/*.cpp.out; do
        for i in `seq 1 10`; do
            echo "Running $file - $i"
            TIME_OUTPUT=$( (time ./$file) 2>&1 )
            real_time=$(echo "$TIME_OUTPUT" | grep real | awk '{print $2}')
            user_time=$(echo "$TIME_OUTPUT" | grep user | awk '{print $2}')
            sys_time=$(echo "$TIME_OUTPUT" | grep sys | awk '{print $2}')
            echo "$file,$i,$real_time,$user_time,$sys_time" >> "$output_csv"
        done;
    done;
done;
