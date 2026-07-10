#include <iostream>
#include <string>
using namespace std;

int main(){
    string ex1  = "Examplesentence";
    cout<< ex1.substr(4,3) << endl; // "mple"
    cout<< ex1[99] << endl;
    int a[2] = {1,2};
    cout << a[3] << endl; // Undefined behavior, out of bounds access
}