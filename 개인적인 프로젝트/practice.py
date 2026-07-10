a = int(input())
num = [int(i) for i in input().split()]
targ = int(input())

count = 0
for i in range(a):
    if targ - i in num:
        count += 1
    
count //= 2

print(count)