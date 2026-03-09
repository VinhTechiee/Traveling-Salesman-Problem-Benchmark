#include "tsm.h"
#include <iostream>

const long long INF = 1000000000000LL;


int vertex_to_index(char vertex_label) {
    if (vertex_label >= 'A' && vertex_label <= 'Z') return vertex_label - 'A';
    if (vertex_label >= 'a' && vertex_label <= 'z') return 26 + (vertex_label - 'a');
    return -1; // Returns -1 if the character is invalid
}

char index_to_vertex(int index) {
    if (index < 26) return 'A' + index;
    return 'a' + (index - 26);
}

bool is_edge_valid(int u, int v, int graph[60][60]) {
    return graph[u][v] > 0;
}

long long tour_cost(const vector<int>& tour, int graph[60][60]) {
    long long cost = 0;
    int n = tour.size();

    if (n < 2) return -1; // Invalid tour

    for (int i = 0; i < n - 1; ++i) {
        int a = tour[i];
        int b = tour[i + 1];

        if (!is_edge_valid(a, b, graph)) return -1; 
        cost += graph[a][b];
    }

    // Check the edge from last to first
    int last = tour[n - 1];
    int first = tour[0];

    if (!is_edge_valid(last, first, graph)) return -1; 
    cost += graph[last][first];

    return cost;
}


// Nearest Neighbor
vector<int> nearest_neighbor(int graph[60][60], int vertices, int start) {
    vector<int> tour;
    vector<bool> visited(vertices, false);
    visited[start] = true;
    tour.push_back(start);
    int current = start;

    for (int step = 1; step < vertices; ++step) {
        int best = -1;
        long long best_dist = INF;

        for (int i = 0; i < vertices; ++i) {
            if (!visited[i] && is_edge_valid(current, i, graph) && graph[current][i] < best_dist) {
                best = i;
                best_dist = graph[current][i];
            }
        }

        if (best == -1) return {}; 

        visited[best] = true;
        tour.push_back(best);
        current = best;
    }
    if (!is_edge_valid(tour.back(), start, graph)) return {}; 
    return tour;
}


void two_opt(vector<int>& tour, int graph[60][60]) {
    int n = tour.size();
    if (n <= 3) return;

    bool improved = true;
    int iteration = 0;
    const int MAX_ITER = 1000;
    long long current_cost = tour_cost(tour, graph);
    if (current_cost == -1) return;

    while (improved && iteration++ < MAX_ITER) {
        improved = false;
        for (int i = 1; i < n - 1; ++i) {
            for (int k = i + 1; k < n; ++k) {
                vector<int> candidate = tour;
                reverse(candidate.begin() + i, candidate.begin() + k + 1);
                
                long long new_cost = tour_cost(candidate, graph);
                if (new_cost != -1 && new_cost < current_cost) {
                    tour.swap(candidate);
                    current_cost = new_cost;
                    improved = true;
                    break; 
                }
            }
            if (improved) break;
        }
    }
}


string Traveling(int graph[60][60], int vertices, char start_char) {
    int start = vertex_to_index(start_char);
    vector<int> best_tour;
    long long best_cost = INF;

    for (int s = 0; s < vertices; ++s) {
        vector<int> tour = nearest_neighbor(graph, vertices, s);
        if (tour.size() != vertices) continue; 
        two_opt(tour, graph);
        long long cost = tour_cost(tour, graph);
        if (cost == -1) continue;
        if (cost != -1 && cost < best_cost) {
            best_cost = cost;
            best_tour = tour;
        }
    }

    if (best_tour.empty()) return ""; 

    if (find(best_tour.begin(), best_tour.end(), start) == best_tour.end()) {
    return ""; 
}

    auto it = find(best_tour.begin(), best_tour.end(), start);
    rotate(best_tour.begin(), it, best_tour.end());

    string result;
    for (int v : best_tour) {
        if (!result.empty()) result += " ";
        result += index_to_vertex(v);
    }
    result += " ";
    result += index_to_vertex(best_tour[0]); 

    return result;
}

string tour_to_string(const vector<int>& tour) {
    if (tour.empty()) return "";
    string result;
    for (int v : tour) {
        if (!result.empty()) result += " ";
        result += index_to_vertex(v);
    }
    result += " ";
    result += index_to_vertex(tour[0]);
    return result;
}

vector<int> brute_force_tsp(int graph[60][60], int vertices, int start) {
    vector<int> nodes;
    for (int i = 0; i < vertices; ++i) {
        if (i != start) nodes.push_back(i);
    }

    vector<int> best_tour;
    long long best_cost = INF;

    sort(nodes.begin(), nodes.end());
    do {
        vector<int> candidate;
        candidate.push_back(start);
        for (int v : nodes) candidate.push_back(v);

        long long cost = tour_cost(candidate, graph);
        if (cost != -1 && cost < best_cost) {
            best_cost = cost;
            best_tour = candidate;
        }
    } while (next_permutation(nodes.begin(), nodes.end()));

    return best_tour;
}