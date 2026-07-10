#ifndef MAZE_DFS_H
#define MAZE_DFS_H

#include <string>
#include <vector>

struct node {
    int x;
    int y;
    std::string path;

    node() {
        x = -1;
        y = -1;
        path = "unreachable";
    }

    node(int a, int b, std::string p) {
        x = a;
        y = b;
        path = p;
    }

    bool operator==(const node& other) const {
        return x == other.x && y == other.y;
    }

    bool operator!=(const node& other) const {
        return !(*this == other);
    }

    bool within_bounds(int n, int m) const {
        return y >= 0 && y < n && x >= 0 && x < m;
    }

    bool next_node_valid(int n, int m, const std::vector<std::vector<int>>& maze, const node& back, const std::vector<node>& visited) const;
};

// Helper struct to hold the path and a visited flag
struct flagged_node {
    std::vector<node> n;
    bool path_found;

    flagged_node(std::vector<node> n, bool v) {
        this->n = n;
        path_found = v;
    }
};

// Helper function declarations
node in_vec(const std::vector<node>& vec, const node& n);
void print_path(const std::vector<node>& path);
bool is_opposite_direction(const std::string& dir1, const std::string& dir2);
flagged_node path_find(std::vector<std::vector<int>> maze, int n, int m);

#endif // MAZE_DFS_H