#ifndef BELLMAN_H
#define BELLMAN_H

#include <vector>
#include <cmath>
#include <string>
#include <fstream>
#include <algorithm> 
#include <random>

using namespace std;

const int MAXV = 60;


int vertex_to_index(char vertex_label);

char index_to_vertex(int index);

void BF(const int graph[MAXV][MAXV], int n, char start, int value[MAXV], int previous[MAXV]);

string buildPath(int startIdx, int goalIdx, const int prev[MAXV]);

string BF_Path(const int graph[MAXV][MAXV], int n, char start, char goal);

#endif
