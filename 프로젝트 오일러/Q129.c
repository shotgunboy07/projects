#include <stdio.h>

int main(){
    int n=17;
    while(1){
        printf("%d\n", n);
        long long int k=1;
        long long int temp=1;
        int flag =0 ;
        while(temp % n != 0){
            temp *= 10;
            k+=temp; // 
            flag++;
        }
        printf("k: %d\n", k);
        if(k>1000000){
            printf("%d", n);
            break;
        }
        else{
            n++;
            while(n%2==0 || n%5==0){
                n++;
            }
        }
    }

    return 0;
}