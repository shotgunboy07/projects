#include <iostream>
using namespace std;

main(){
    int n,m;
    cin >> n >> m;
    int a = 100*m/n; 

    if(n==m){
        cout<<-1<<endl;
        return 0;
    }

    cout << n << " " << m << " " << a << endl;
    int count = 0;
    while(true){
        cout << int(100*m/n) << endl;
        if(a == int(100*m/n)){
            count++; m++; n++;
        } 
        else{
            cout << count << endl;
            return 0;
        }
    }
    
}