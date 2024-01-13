
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Example script to demonstrate argparse usage.")

# Add the '-N' argument
parser.add_argument('-E', type=int, help="2 >> (E)xponent")

# Parse the arguments
args = parser.parse_args()

BENCHMARKS_DIR="benchmarks"
N=2**args.E

body = '''

#include <iostream>
#include <map>
#include <tuple>
#include <vector>
#include <unordered_map>

{{map_declaration}}

int main() {
  std::vector<int> v = {
#include "foo.csv"
  };

  {{map_loop}}

  return 0;
}

'''

def nested_map_declaration(map_type, depth):
    declaration = ""
    for i in range(0, depth):
        declaration = f"{declaration}std::{map_type}<int, "
    declaration = f"{declaration}int"
    for i in range(0, depth):
        declaration = f"{declaration}>"
    declaration = f"{declaration} m;"
    return declaration

def nested_map_loop(depth):
    n = int(round(N**(1/depth)))
    loop = ""
    for i in range(0, depth):
        loop = f"""{loop}{'  ' * (i+1)}for (int x{i} = 0; x{i} < {n}; x{i}++) {{\n"""
    loop = f"{loop}{'  '*(depth+1)}m{''.join([f'[{i}]' for i in range(0, depth)])} = 1;"
    for i in range(0, depth):
        loop = f"{loop}\n{'  ' * (depth-i+1)}}}"
    return loop



def nested_templated_map_declaration(map_type, depth):
    declaration = f"""

// Forward declaration of the template class
template <typename... Args>
class MultiLevelMap;

// Specialization for container types like std::vector
template <typename TKey, typename TValue>
class MultiLevelMap<TKey, TValue> {{
 public:
  TValue& operator[](const TKey& key) {{ return data[key]; }}
 private:
  std::{map_type}<TKey, TValue> data;
}};

// Recursive variadic template specialization
template <typename TKey, typename... TKeys>
class MultiLevelMap<TKey, TKeys...> {{
 public:
MultiLevelMap<TKeys...>& operator[](const TKey& key) {{ return data[key]; }}
 private:
  std::{map_type}<TKey, MultiLevelMap<TKeys...>> data;
}};

MultiLevelMap<"""
    for i in range(0, depth):
        declaration = f"{declaration}int, "
    declaration = f"{declaration}int>"
    declaration = f"{declaration} m;"
    return declaration



def tuple_map_declaration(map_type, depth):
    declaration = f"""
struct tuple_operations {{
    // Comparator for std::map
    template <typename... Args>
    bool operator() (const std::tuple<Args...>& a, const std::tuple<Args...>& b) const {{
        return a < b;
    }}

    // Hash function for std::unordered_map
    template <typename... TupleArgs>
    std::size_t operator()(const std::tuple<TupleArgs...>& t) const {{
        return hash_value(t, std::index_sequence_for<TupleArgs...>{{}});
    }}

private:
    // Hash value computation
    template <typename TupleType, size_t... I>
    std::size_t hash_value(const TupleType& t, std::index_sequence<I...>) const {{
        return combine(std::hash<std::tuple_element_t<I, TupleType>>{{}}(std::get<I>(t))...);
    }}

    // Recursive function to combine hash values
    std::size_t combine(std::size_t first) const {{
        return first;
    }}

    template <typename... Rest>
    std::size_t combine(std::size_t first, Rest... rest) const {{
        auto seed = combine(rest...);
        return first ^ (seed << 1);
    }}
}};
std::{map_type}<std::tuple<{', '.join([f'int' for i in range(0, depth)])}"""
    declaration = f"{declaration}>, int, tuple_operations>"
    declaration = f"{declaration} m;"
    return declaration

def tuple_map_loop(depth):
    n = int(round(N**(1/depth)))
    loop = ""
    for i in range(0, depth):
        loop = f"{loop}{'  ' * (i+1)}for (int x{i} = 0; x{i} < {n}; x{i}++) {{\n"
    loop = f"{loop}{'  '*(depth+1)}m[std::make_tuple({', '.join([f'{i}' for i in range(0, depth)])})] = 1;"
    for i in range(0, depth):
        loop = f"{loop}\n{'  ' * (depth-i+1)}}}"
    return loop

config = [
    ("map", "nested", nested_map_declaration, nested_map_loop),
    ("map", "nested_templated", nested_templated_map_declaration, nested_map_loop),
    ("map", "tuple", tuple_map_declaration, tuple_map_loop),
    ("unordered_map", "nested", nested_map_declaration, nested_map_loop),
    ("unordered_map", "nested_templated", nested_templated_map_declaration, nested_map_loop),
    ("unordered_map", "tuple", tuple_map_declaration, tuple_map_loop)
]


if __name__ == "__main__":
    for (map_type, approach, map_declaration, map_loop) in config:
        for i in [1, 2, 4, 8, 16]:
            declaration = map_declaration(map_type, i)
            loop = map_loop(i)
            result = body.replace("{{map_declaration}}", declaration)
            result = result.replace("{{map_loop}}", loop)
            with open(f"{BENCHMARKS_DIR}/{map_type}/{approach}/{i}.cpp", "w") as file:
                file.write(result)


# # Generate Distribution:
# randomNums = np.random.normal(scale=5500, size=200) + 20000
# randomInts = np.round(randomNums)

# # Plot:
# plt.hist(randomInts)
# plt.savefig("foo.png")

# df = pd.DataFrame(randomInts)
# df.to_csv("foo.csv", index=False, header=False)
