
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

body = '''

#include <iostream>
#include <map>
#include <tuple>
#include <vector>

{{map_declaration}}

int main() {
  std::vector<int> array = {
#include "../foo.csv"
  };

  {{map_loop}}

  return 0;
}

'''

def nested_map_declaration(depth):
    declaration = ""
    for i in range(0, depth):
        declaration = f"{declaration}std::map<int, "
    declaration = f"{declaration}int"
    for i in range(0, depth):
        declaration = f"{declaration}>"
    declaration = f"{declaration} m;"
    return declaration

def nested_map_loop(depth):
    loop = ""
    for i in range(0, depth):
        loop = f"""{loop}{'  ' * (i+1)}for (int x{i} = 0; x{i} < {depth}; x{i}++) {{\n"""
    loop = f"{loop}{'  ' * (depth+2)}m"
    for i in range(0, depth):
        loop = f"{loop}[x{i}]"
    loop = f"{loop} = 1;"
    for i in range(0, depth):
        loop = f"{loop}\n{'  ' * (depth-i+1)}}}"
    return loop



def nested_templated_map_declaration(depth):
    declaration = """

// Forward declaration of the template class
template <typename... Args>
class MultiLevelMap;

// Specialization for container types like std::vector
template <typename TKey, typename TValue>
class MultiLevelMap<TKey, TValue> {
 public:
  TValue& operator[](const TKey& key) { return data[key]; }
 private:
  std::map<TKey, TValue> data;
};

// Recursive variadic template specialization
template <typename TKey, typename... TKeys>
class MultiLevelMap<TKey, TKeys...> {
 public:
MultiLevelMap<TKeys...>& operator[](const TKey& key) { return data[key]; }
 private:
  std::map<TKey, MultiLevelMap<TKeys...>> data;
};

MultiLevelMap<"""
    for i in range(0, depth):
        declaration = f"{declaration}int, "
    declaration = f"{declaration}int>"
    declaration = f"{declaration} m;"
    return declaration



def tuple_map_declaration(depth):
    declaration = "std::map<std::tuple<int"
    for i in range(0, depth):
        declaration = f"{declaration}, int"
    declaration = f"{declaration}>, int>"
    declaration = f"{declaration} m;"
    return declaration

def tuple_map_loop(depth):
    loop = ""
    for i in range(0, depth):
        loop = f"""{loop}{'  ' * (i+1)}for (int x{i} = 0; x{i} < {depth}; x{i}++) {{\n"""
    loop = f"{loop}{'  ' * (depth+2)}m[std::make_tuple(x0"
    for i in range(0, depth-1):
        loop = f"{loop}, x{i}"
    loop = f"{loop}, x{depth-1})] = 1;"
    for i in range(0, depth):
        loop = f"{loop}\n{'  ' * (depth-i+1)}}}"
    return loop

config = [
    ("nested", nested_map_declaration, nested_map_loop),
    ("nested_templated", nested_templated_map_declaration, nested_map_loop),
    ("tuple", tuple_map_declaration, tuple_map_loop)
]

for (name, map_declaration, map_loop) in config:
    for i in range(1, 9):
        declaration = map_declaration(i)
        loop = map_loop(i)
        result = body.replace("{{map_declaration}}", declaration)
        result = result.replace("{{map_loop}}", loop)
        with open(f"{name}/{name}{i}.cpp", "w") as file:
            file.write(result)


# # Generate Distribution:
# randomNums = np.random.normal(scale=5500, size=200) + 20000
# randomInts = np.round(randomNums)

# # Plot:
# plt.hist(randomInts)
# plt.savefig("foo.png")

# df = pd.DataFrame(randomInts)
# df.to_csv("foo.csv", index=False, header=False)
