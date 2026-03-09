#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <chrono>
#include <random>
#include "tsm.h"

using namespace std;
using namespace std::chrono;

static const int MAXN = 60;

void generate_complete_graph(int graph[MAXN][MAXN], int n, int minW, int maxW, mt19937& rng) {
    uniform_int_distribution<int> dist(minW, maxW);

    for (int i = 0; i < MAXN; ++i)
        for (int j = 0; j < MAXN; ++j)
            graph[i][j] = 0;

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i != j) graph[i][j] = dist(rng);
        }
    }
}

long long measure_nn(int graph[MAXN][MAXN], int n, int start, long long& runtime_us) {
    auto t1 = high_resolution_clock::now();
    vector<int> tour = nearest_neighbor(graph, n, start);
    auto t2 = high_resolution_clock::now();

    runtime_us = duration_cast<microseconds>(t2 - t1).count();
    if ((int)tour.size() != n) return -1;
    return tour_cost(tour, graph);
}

long long measure_nn_2opt(int graph[MAXN][MAXN], int n, int start, long long& runtime_us) {
    auto t1 = high_resolution_clock::now();
    vector<int> tour = nearest_neighbor(graph, n, start);
    if ((int)tour.size() == n) {
        two_opt(tour, graph);
    }
    auto t2 = high_resolution_clock::now();

    runtime_us = duration_cast<microseconds>(t2 - t1).count();
    if ((int)tour.size() != n) return -1;
    return tour_cost(tour, graph);
}

long long measure_bruteforce(int graph[MAXN][MAXN], int n, int start, long long& runtime_us) {
    auto t1 = high_resolution_clock::now();
    vector<int> tour = brute_force_tsp(graph, n, start);
    auto t2 = high_resolution_clock::now();

    runtime_us = duration_cast<microseconds>(t2 - t1).count();
    if ((int)tour.size() != n) return -1;
    return tour_cost(tour, graph);
}

int main() {
    mt19937 rng(42);
    ofstream fout("results.csv");

    fout << "n,test_id,nn_cost,nn_time_us,nn2opt_cost,nn2opt_time_us,bruteforce_cost,bruteforce_time_us\n";

    // brute force chỉ nên dùng tới khoảng n = 9 hoặc 10
    vector<int> sizes = {5, 6, 7, 8, 9};
    const int TESTS_PER_SIZE = 20;
    const int start = 0;

    for (int n : sizes) {
        for (int test_id = 1; test_id <= TESTS_PER_SIZE; ++test_id) {
            int graph[MAXN][MAXN];
            generate_complete_graph(graph, n, 1, 100, rng);

            long long nn_time = 0, nn2opt_time = 0, bf_time = 0;
            long long nn_cost = measure_nn(graph, n, start, nn_time);
            long long nn2opt_cost = measure_nn_2opt(graph, n, start, nn2opt_time);
            long long bf_cost = measure_bruteforce(graph, n, start, bf_time);

            fout << n << ","
                 << test_id << ","
                 << nn_cost << "," << nn_time << ","
                 << nn2opt_cost << "," << nn2opt_time << ","
                 << bf_cost << "," << bf_time << "\n";

            cout << "n=" << n
                 << ", test=" << test_id
                 << ", NN cost=" << nn_cost
                 << ", NN+2opt cost=" << nn2opt_cost
                 << ", BF cost=" << bf_cost
                 << endl;
        }
    }

    fout.close();
    cout << "Saved benchmark results to results.csv\n";
    return 0;
}