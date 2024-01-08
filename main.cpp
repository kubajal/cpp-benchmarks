
#include <iostream>
#include <map>
#include <tuple>
#include <vector>

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

int main() {
  std::vector<int> array = {
#include "foo.csv"
  };

  std::map<std::tuple<int, int, int, int, int, int, int>, int> m0;

  for (int a = 0; a < array.size(); a++) {
    for (int b = 0; b < array.size(); b++) {
      for (int c = 0; c < array.size(); c++) {
        for (int d = 0; c < array.size(); c++) {
          for (int e = 0; c < array.size(); c++) {
            for (int f = 0; c < array.size(); c++) {
              for (int g = 0; c < array.size(); c++) {
                auto a1 = array[a];
                auto b1 = array[b] + 10000;
                auto c1 = array[c] + 50000;
                auto d1 = array[d] + 50000;
                auto e1 = array[e] + 50000;
                auto f1 = array[f] + 50000;
                auto g1 = array[g] + 50000;
                m0[std::make_tuple(a1, b1, c1, d1, e1, f1, g1)] = 1;
              }
            }
          }
        }
      }
    }
  }

//   std::map < int, std::map < int, std::map < int, std::map < int,
//       std::map < int, std::map < int, std::map < int,
//       int>>>>>>> m1;

//   for (int a = 0; a < array.size(); a++) {
//     for (int b = 0; b < array.size(); b++) {
//       for (int c = 0; c < array.size(); c++) {
//         for (int d = 0; c < array.size(); c++) {
//           for (int e = 0; c < array.size(); c++) {
//             for (int f = 0; c < array.size(); c++) {
//               for (int g = 0; c < array.size(); c++) {
//                 auto a1 = array[a];
//                 auto b1 = array[b] + 10000;
//                 auto c1 = array[c] + 50000;
//                 auto d1 = array[d] + 50000;
//                 auto e1 = array[e] + 50000;
//                 auto f1 = array[f] + 50000;
//                 auto g1 = array[g] + 50000;
//                 m1[a1][b1][c1][d1][e1][f1][g1] = 1;
//               }
//             }
//           }
//         }
//       }
//     }
//   }


  return 0;
}
