#include <iostream>
#include <iomanip>
#include <stdio.h>
using namespace std;
typedef long long int lli;

struct largeint {
    lli front = 0; // 뒤 10자리 제외 앞자리 전체
    lli back  = 0;  // 뒤 10자리
};

int cmplargeint(largeint a, largeint b) {
    //a가 크면 1, b가 크면 -1, 같으면 0
    if (a.front > b.front) {
        return 1;
    }
    else if (a.front < b.front) {
        return -1;
    }
    else {
        if (a.back > b.back) {
            return 1;
        }
        else if (a.back < b.back) {
            return -1;
        }
        else {
            return 0;
        }
    }
}

largeint operator*(largeint a, int b) {
    largeint result;
    result.front = a.front * b;
    result.back = a.back * b;
    result.front += result.back / 100000000;
    result.back %= 100000000;
    return result;
}

largeint power(int base, int exponent) {
    // base = 밑 , exponent = 지수
    largeint result;
    result.back = 1;
    for (int i = 0; i < exponent; i++) {
        result = result*base;
    }
    return result;
}

void printlargeint(largeint a) {
    if (a.front == 0) {
        cout << a.back << endl;
    }
    else {
        cout << a.front << a.back << endl;
    }
}
int main(){
    int count = 0;
    for(int i = 1; i < 10; i++){ //밑
        for(int j = 1; ; j++){ //지수
            if(cmplargeint(power(10,j-1),power(i, j)) != 1 && cmplargeint(power(10,j),power(i, j)) == 1){
                printf("%d^%2d = ", i, j);
                printlargeint(power(i, j));
                count++;
            }
            else{
                break;
            }
        }
    }
    cout<<count<<endl;
    return 0;
}