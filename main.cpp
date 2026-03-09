#include <iostream>
#include <string>
#include "bellman.h"
#include "tsm.h"

using namespace std;

int main() {
    
    int graph[MAXV][MAXV] = {0}; // Default to 0 (no edges)
    int n = 5; // Number of vertices in the graph

    // Assume the graph is a weighted adjacency matrix
    graph[0][1] = 10;  // A -> B with weight 10
    graph[1][2] = 20;  // B -> C with weight 20
    graph[2][3] = 30;  // C -> D with weight 30
    graph[3][4] = 40;  // D -> E with weight 40
    graph[4][0] = 50;  // E -> A with weight 50
    graph[0][2] = 15;  // A -> C with weight 15


   // Initialize Value and Previous arrays
    int value[MAXV], previous[MAXV];
    for (int i = 0; i < n; ++i) {
        value[i] = -1; 
        previous[i] = -1; 
    }

    char start = 'A'; // Starting vertex
    char goal = 'D';  // Goal vertex

    // Run Bellman-Ford algorithm
    BF(graph, n, start, value, previous);

   // Output the shortest path from start to goal
    string path = BF_Path(graph, n, start, goal);
    if (path.empty()) {
        cout << "No path found from " << start << " to " << goal << endl;
    } else {
        cout << "Path from " << start << " to " << goal << ": " << path << endl;
    }

    
    // Solve the Traveling Salesman Problem (TSP)
    string tsp_result = Traveling(graph, n, start);  // Call the TSP function
    if (!tsp_result.empty()) {
        cout << "Traveling Salesman Path: " << tsp_result << endl;
    } else {
        cout << "No valid TSP tour found." << endl;
    }

    return 0;
}