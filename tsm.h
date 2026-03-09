#ifndef TSM_H
#define TSM_H

#include <vector>
#include <cmath>
#include <string>
#include <fstream>
#include <algorithm> 
#include <random>
using namespace std;


int vertex_to_index(char vertex_label);

char index_to_vertex(int index);

bool is_edge_valid(int u, int v, int graph[60][60]);

long long tour_cost(const vector<int>& tour, int graph[60][60]);

vector<int> nearest_neighbor(int graph[60][60], int vertices, int start);

void two_opt(vector<int>& tour, int graph[60][60]);

string Traveling(int graph[60][60], int vertices, char start_char);

// Benchmark helpers
vector<int> brute_force_tsp(int graph[60][60], int vertices, int start);
string tour_to_string(const vector<int>& tour);

#endif