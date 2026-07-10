#include <iostream>
#include <string>
#include <vector>
#include "maze_DFS.h"
using namespace std;


// DFS search finds a path from (0,0) to (n-1,m-1) in a maze represented as a 2D vector. The maze is represented as a 2D vector of integers, where 0 represents an open cell and 1 represents a blocked cell. 
// The function returns a flagged_node struct containing the path and a boolean indicating whether a path was found or not. 
// The path is represented as a vector of node structs, where each node contains the x and y coordinates of the cell and the direction taken to reach that cell.

// Helper function to check if a node is in a vector of nodes
node in_vec(const vector<node>& vec, const node& n) {
    for( const auto& node : vec) {
        if (node.x == n.x && node.y == n.y) {
            return node;
        }
    }
    return node(-1, -1, "not found");
}


// Check if the next node is within bounds, not visited, and not blocked. If any of these conditions are not met, return false. Otherwise, return true.
bool node::next_node_valid(int n, int m, const vector<vector<int>>& maze, const node& back, const vector<node>& visited) const {

        // Get the next node based on the last visited node's path
        node next = back;
        if ( next.path == "N"){
            next.y -= 1;
        }
        else if ( next.path == "S"){
            next.y += 1;
        }
        else if ( next.path == "E"){
            next.x += 1;
        }
        else if ( next.path == "W"){
            next.x -= 1;
        }


        if (!next.within_bounds(n, m)) { // Check if the next node is within bounds
            // cout << "Next node (" << next.x << "," << next.y << ") is out of bounds." << endl;
            return false;
        }
        else if (maze[next.y][next.x] == 1) { // Check if the next node is blocked. Because maze is a 2D vector, we access it using maze[y][x]
            // cout << "Next node (" << next.x << "," << next.y << ") is blocked." << endl;
            return false;
        }
        else if (in_vec(visited, next) != node(-1, -1, "not found")) { // Check if the next node has already been visited
            // cout << "Next node (" << next.x << "," << next.y << ") has already been visited" << endl;
            return false;
        }

        return true;
    }

// Helper function to print the path
void print_path(const vector<node>& path) {
    for (const auto& node : path) {
        cout << "(" << node.x << "," << node.y << "," << node.path << ") ";
    }
    cout << endl;
}

// Helper function to check if two directions are opposite. In path_find, this is used to check if the current node has tried all directions and needs to backtrack.
bool is_opposite_direction(const string& dir1, const string& dir2) {
    return (dir1 == "N" && dir2 == "S") || (dir1 == "S" && dir2 == "N") ||
           (dir1 == "E" && dir2 == "W") || (dir1 == "W" && dir2 == "E");
}

flagged_node path_find( vector<vector<int>> maze, int n, int m ){
    // Return DFS path from (0,0) to (n-1,m-1) if exists, else return empty vector with initial node with direction marked as "unreachable"
    vector<node> s;
    vector<node> visited;
    const string directions[] = {"E", "S", "W", "N"};
    if (maze[0][0] == 1){
        return flagged_node({node(0,0,"unreachable")}, false);
    }
    s.push_back(node(0,0,"E"));
    visited.push_back(node(0,0,"E"));   
    
    while(true){
        // Debugging output
        // cout << "Current stack: ";
        // print_path(s);

        // pass 1 : If stack reackes (n-1,m-1), return path
        if(s.back().y == n-1 && s.back().x == m-1){
            // cout << "Path found at pass 1: ";
            // print_path(s);
            return flagged_node(s, true);
        }

        // pass 2 : If stack is empty, return "unreachable"
        if(s.empty()){
            // cout << "Path not found at pass 2: ";
            return flagged_node(visited, false);
        } 

        // pass 3 : If next node is valid(within bounds, not visited, not blocked), push it to stack and continue DFS
        if(s.back().next_node_valid(n, m, maze, s.back(), visited)){
            node next = s.back();
            if (s.back().path == "N"){
                next.y -= 1;
                next.path = "W";
            }
            else if (s.back().path == "S"){
                next.y += 1;
                next.path = "E";
            }
            else if (s.back().path == "E"){
                next.x += 1;
                next.path = "N";
            }
            else if (s.back().path == "W"){
                next.x -= 1;
                next.path = "S";
            }

            // Debugging output
            // cout << "Next node (" << next.x << "," << next.y << ") is valid. Pushing to stack." << endl;

            s.push_back(next);
            visited.push_back(next);
            continue;
        }

        // pass 4 : If next node is not valid, move to next direction clockwise and continue DFS
        else{
            if (s.back().path == "N"){
                s.back().path = "E";
            }
            else if (s.back().path == "E"){
                s.back().path = "S";
            }
            else if (s.back().path == "S"){
                s.back().path = "W";
            }
            else if (s.back().path == "W"){
                s.back().path = "N";
            }
            //pass 5 : Edge case / For the first node, if all directions(which is only E & S) have been tried, return "unreachable"
            if (s.size() == 1 && s.back().path == "W"){
                // cout << "All directions tried for the first node. Returning unreachable." << endl;
                return flagged_node(visited, false);
            }

            // pass 6 : If all directions have been tried, pop the stack and continue DFS
            else if(s.size() > 1){
                node prev = s[s.size()-2];
                if( is_opposite_direction(prev.path, s.back().path)){
                    /* Debugging output 
                    cout << "prev node (" << prev.x << "," << prev.y << "," << prev.path << ")" << endl;
                    cout << "All directions tried for node (" << s.back().x << "," << s.back(   ).y << "). Popping from stack." << endl;
                    */

                s.pop_back();
                }
            }
        }
    }

    return flagged_node(s, true);
 

}

int main() {
    int n,m;
    cin >> n >> m;
    vector<vector<int>> maze(n, vector<int>(m));
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++){
            cin >> maze[i][j];
        }
    }

    flagged_node path = path_find(maze, n, m);
    puts("");
    if(!path.path_found){
        for (int i=0; i<n; i++){
            for (int j=0; j<m; j++){
                bool is_path = false;
                for (int k=0;k<path.n.size();k++){
                    const auto& node = path.n[k];
                    if (node.x == j && node.y == i){
                        is_path = true;
                        break;
                    }
                }
                if (is_path){
                    cout << "\033[1;31m" << maze[i][j] << "\033[0m "; // Red color for visited nodes with dead ends 
                }
                else{
                    cout << maze[i][j] << " ";
                }
            }
            cout << endl;
        }
    }
    else{
        /*  Naive path print
        cout << "(" << path[0].x << " " << path[0].y << ")";
        for (int i=1;i<path.size();i++){
            cout << " ->" << " (" << path[i].x << " " << path[i].y << ")";
            
        }
        */

        // better printing with colored output
        for (int i=0; i<n; i++){
            for (int j=0; j<m; j++){
                bool is_path = false;
                for (const auto& node : path.n){
                    if (node.x == j && node.y == i){
                        is_path = true;
                        break;
                    }
                }
                if (is_path){
                    cout << "\033[1;32m" << maze[i][j] << "\033[0m "; // Green color for path
                }
                else{
                    cout << maze[i][j] << " ";
                }
            }
            cout << endl;
        }
    }

    return 0;
}
