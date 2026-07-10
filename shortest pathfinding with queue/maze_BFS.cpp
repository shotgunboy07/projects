#include <iostream>
#include <string>
#include <vector>
#include <deque>
#include <stack>
using namespace std;

struct node{
    int x;
    int y;
    int branch_count;
    node* parent;

    // Constructor
    node(int x, int y, int branch_count, node* parent) : x(x), y(y), branch_count(branch_count), parent(parent) {}
    bool operator==(const node& other) const {
        return x == other.x && y == other.y;
    }
};

node* find_shortest_path( vector<vector<int>>& maze, int n, int m ){
    const pair<int, int> directions[4] = {
        {0, -1}, // North
        {1, 0},  // East
        {0, 1},  // South
        {-1, 0}  // West
        
    };

    deque<node*> q;
    q.push_back(new node(0, 0, 0, nullptr));

    // Trivial case: If the start or end is a wall, return nullptr
    if (maze[0][0] == 1 || maze[n-1][m-1] == 1) {
        cout << "No path found." << endl;
        return nullptr; // No path if start or end is a wall
    }

    // Trivial case: If the start is the same as the end, return the start node
    if (n == 1 && m == 1 && maze[0][0] == 0) {
        return new node(0, 0, 0, nullptr); // Return the start node
    }
    maze[0][0] = 1; // Mark the starting node as visited

   while (true) {

        node* current = q.front();
        cout << "Current node: (" << current->x << "," << current->y << ")" << endl;
        // test direction
        for(const auto& dir : directions) {
            int new_x = current->x + dir.first;
            int new_y = current->y + dir.second;
            cout << "Checking node: (" << new_x << "," << new_y << ")" << endl;

            // node validation : Within bounds and not a wall(or visited)
            if (new_x >= 0 && new_x < m && new_y >= 0 && new_y < n && maze[new_y][new_x] == 0) {
                maze[new_y][new_x] = 1; // Mark as visited. Now, visited nodes are also marked as 1 as well as walls.
                cout << "Adding node: (" << new_x << "," << new_y << ")" << endl;
                q.push_back(new node(new_x, new_y, 0, current));
                current->branch_count++;
            }

            // Check if the new position is the destination
            if (new_x == m - 1 && new_y == n - 1) {
                cout << "Destination reached at node: (" << new_x << "," << new_y << "). Deletion sequence initiated." << endl;
                q.pop_front();
                // Delete all nodes in the queue and it's links all the way down until it reaches it's nearest branch 
                while(q.size() != 1){
                    node* target = q.front();
                    q.pop_front();
                    while (target->x != 0 || target->y != 0) { // Stop when we reach the root node
                        node* temp = target;
                        target = target->parent;
                        cout << "Deleting node: (" << temp->x << "," << temp->y << ")" << endl;
                        delete temp; // Free memory
                        if (target->branch_count-- > 1) {
                            break; // Stop if we reach a branch node
                        }
                    }
                    cout << endl;
                }

                return new node(m - 1, n - 1, 0, current); // Return the destination node

            }

        }
        

        // If the current node has no directions to go, delete it and all its parents until it reaches a branch node.
        if (current->branch_count == 0) {
            cout << "No valid directions from node: (" << current->x << "," << current->y << "). Deletion sequence initiated." << endl;
            node* target = current;
            while (target->x != 0 || target->y != 0) { // Stop when reaching the starting node
                node* temp = target;
                target = target->parent;
                cout << "Deleting node: (" << temp->x << "," << temp->y << ")" << endl;
                delete temp; // Free memory
                if (target->branch_count-- > 1) {
                    break; // Stop if we reach a branch node
                }
            }
            cout << endl;
        }

        q.pop_front();

        if ( q.empty() ) return nullptr; // No path found
            

        // print q
        cout << "Queue: ";
        for (const auto& node_ptr : q) {
            cout << "(" << node_ptr->x << "," << node_ptr->y << ") ";
        }
        cout << endl;

        //print all possible paths atp
        cout << "Possible Paths: \n";
        for (const auto& node_ptr : q) {
            stack<node*> path_stack;
            node* temp = node_ptr;
            while (temp != nullptr) {
                path_stack.push(temp);
                temp = temp->parent;
            }
            cout << "[";
            while (!path_stack.empty()) {
                node* path_node = path_stack.top();
                path_stack.pop();
                cout << "(" << path_node->x << "," << path_node->y << ")";
                if (!path_stack.empty()) {
                    cout << " -> ";
                }
            }
            cout << "] \n";
        }
        cout << endl;
        
    }
}
 
int main(){

    // freopen("input.txt", "r", stdin);
    int n,m;
    cin >> n >> m;
    vector<vector<int>> maze(n, vector<int>(m));
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++){
            cin >> maze[i][j];
        }
    }

    node* result = find_shortest_path(maze, n, m);
    string path = "";

    if (result == nullptr) {
        cout << "No path found." << endl;
        return 0;
    }

    cout << "Shortest Path: ";
    while (result != nullptr) {
        path = "(" + to_string(result->x) + "," + to_string(result->y) + ")" + (path.empty() ? "" : " -> ") + path;
        result = result->parent;
    }
    cout << path << endl;
}