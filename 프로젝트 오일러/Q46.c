#include <stdio.h>
#include <stdlib.h> 
int howmanyprimenumbersundertest(int test) 
{
    int count = 0;
    for (int i = 2; i <= test; i++) {
        int isprime = 1;
        for (int j = 2; j < i; j++) {
            if (i % j == 0) {
                isprime = 0;
                break;
            }
        }
        if (isprime) {
            count++;
        }
    }
    return count;
}

int howmanysqauaresundertest(int test) 
{
    int count = 0;
    for (int i = 1; i <= test; i++) {
        if (i * i <= test) {
            count++;
        }
        else {
            break;
        }
    }
    return count;
}

void* allprimenumbersundertest(int *array, int test) 
{
    int count = 0;
    for (int i = 2; i <= test; i++) {
        int isprime = 1;
        for (int j = 2; j < i; j++) {
            if (i % j == 0) {
                isprime = 0;
                break;
            }
        }
        if (isprime) {
            array[count] = i;
            count++;
        }
    }
}

void* allsquaresundertest(int *array, int test) 
{
    for (int i=1; i <= howmanysqauaresundertest(test); i++) {
        array[i-1] = i * i;
    }
}

int isprime(int test) 
{
    int isprime = 1;
    for (int i = 2; i < test; i++) {
        if (test % i == 0) {
            isprime = 0;
            break;
        }
    }
    if (isprime) {
        return 1; // return if prime
    }
    else {
        return 0; // return if not prime
    }
}



int main() {
    int test = 35;
    while(1) {
        int temp = 0;
        int ret1[howmanyprimenumbersundertest(test)] ;
        int ret2[howmanysqauaresundertest(test)] ;
        allprimenumbersundertest(ret1, test);
        allsquaresundertest(ret2, test);
        int totalcombinations = 0;
        for(int i = 0; i < howmanyprimenumbersundertest(test); i++) {
            temp = ret1[i];
            for(int j = 0; j < howmanysqauaresundertest(test); j++) {
                temp += (2*ret2[j]);
                if(temp == test) {
                    printf("%d = %d + 2*%d\n", test, ret1[i], ret2[j]);
                    do {
                        test += 2;
                    } while( isprime(test) == 1 );
                }
                else {
                    totalcombinations++;
                    temp = ret1[i];
                }
            }
        }
        if(totalcombinations == howmanyprimenumbersundertest(test) * howmanysqauaresundertest(test)) {
            printf("The number %d cannot be expressed as the sum of a prime number and twice a square.\n", test);
            break;
        }
    } 
}