#include "bellman.h"

const int MAXV = 60;

// Converts a character representing a vertex to its index
int vertex_to_index(char vertex_label) {
    if (vertex_label >= 'A' && vertex_label <= 'Z') return vertex_label - 'A';
    if (vertex_label >= 'a' && vertex_label <= 'z') return 26 + (vertex_label - 'a');
    return -1; // Returns -1 if the character is invalid
}

// Converts an index back to a character representing a vertex
char index_to_vertex(int index) {
    if (index < 26) return 'A' + index;
    return 'a' + (index - 26);
}


void BF(const int graph[MAXV][MAXV], int n, char start, int value[MAXV], int previous[MAXV]) {
    int s = vertex_to_index(start);  
    
    if (s < 0 || s >= n) return;  

    
    if (value[s] == -1) {
        for (int i = 0; i < n; ++i) {
            if (value[i] == -1) {
                value[i] = -1;  
                previous[i] = -1;    
            }
        }
        value[s] = 0;  
        previous[s] = -1;
    }

    int newValue[MAXV], newPrev[MAXV];
    
    for (int i = 0; i < n; ++i) {
        newValue[i] = value[i];
        newPrev[i] = previous[i];
    }

    for (int u = 0; u < n; ++u) {
        if (value[u] == -1) continue;  

        for (int v = 0; v < n; ++v) {
            if (u == v || graph[u][v] <= 0) continue;  
            int weight = graph[u][v];
            long long candidate = (long long)value[u] + weight;
            
            if (candidate < newValue[v] || newValue[v] == -1) {
                newValue[v] = (int)candidate;
                newPrev[v] = u;
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        value[i] = newValue[i];
        previous[i] = newPrev[i];
    }
}


static string buildPath(int startIdx, int goalIdx, const int prev[MAXV]) {
    vector<int> rev;
    for (int cur = goalIdx; cur != -1 && cur != startIdx; cur = prev[cur]) rev.push_back(cur);
    if (rev.empty() && goalIdx != startIdx && prev[goalIdx] == -1) return ""; 

    string out;
    out.push_back(index_to_vertex(startIdx));
    for (int i = (int)rev.size() - 1; i >= 0; --i) {
        out.push_back(' ');
        out.push_back(index_to_vertex(rev[i]));
    }
    return out;
}


string BF_Path(const int graph[MAXV][MAXV], int n, char start, char goal) {
    int s = vertex_to_index(start), g = vertex_to_index(goal);
    if (s < 0 || s >= n || g < 0 || g >= n) return "";

    int dist[MAXV], prev[MAXV];
    for (int i = 0; i < n; ++i) { dist[i] = -1; prev[i] = -1; }
    dist[s] = 0;

    // Bellman-Ford algorithm
    for (int pass = 0; pass < n - 1; ++pass) {
        bool improved = false;
        int oldDist[MAXV];
        for (int i = 0; i < n; ++i) oldDist[i] = dist[i];

        for (int u = 0; u < n; ++u) {
            if (oldDist[u] == -1) continue; 
            for (int v = 0; v < n; ++v) {
                if (u == v) continue;
                int w = graph[u][v];
                if (w == 0) continue;       
                long long cand = (long long)oldDist[u] + w;
                if (dist[v] == -1 || cand < dist[v]) {
                    dist[v] = (int)cand;
                    prev[v] = u;
                    improved = true;
                }
            }
        }
        if (!improved) break; 
    }

    if (dist[g] == -1) return "";  
    return buildPath(s, g, prev);
}
