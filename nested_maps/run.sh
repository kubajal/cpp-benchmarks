
set -x
set -e

BENCHMARKS_DIR=benchmarks

if [ ! -d benchmarks ] ; then

    for map_type in unordered_map map; do
        for approach in nested nested_templated tuple; do
            mkdir -p "$BENCHMARKS_DIR/$map_type/$approach"
        done
    done

    echo "Generating cpp files"
    python preprocess.py -E 16

    echo "Compiling C++ files"
    find . -name *.cpp | xargs -I{} g++ {} -I`pwd` -o {}.out
fi

echo "Executing measurements"
output_csv="out.csv"
echo "path,type_name,i,depth,real_time,user_time,sys_time" > $output_csv
for map_type in "map" "unordered_map"; do
    for approach in "nested" "nested_templated" "tuple"; do
        for file in benchmarks/$map_type/$approach/*.cpp.out; do
            base=$(basename "$file")
            depth="${base%.cpp.out}"
            for i in `seq 1 100`; do
                echo "Running $file - $i"
                TIME_OUTPUT=$( (time ./$file) 2>&1 )
                real_time=$(echo "$TIME_OUTPUT" | grep real | awk '{print $2}')
                user_time=$(echo "$TIME_OUTPUT" | grep user | awk '{print $2}')
                sys_time=$(echo "$TIME_OUTPUT" | grep sys | awk '{print $2}')
                echo "$file,$map_type/$approach,$i,$depth,$real_time,$user_time,$sys_time" >> "$output_csv"
            done;
        done;
    done;
done;

echo "Postprocessing the CSV, generating a real_time vs. size graph..."

python postprocess.py
