

def iterateAndReturn(list):
    sum = 0
    listRange = range(0,len(list),1)
    for i in listRange:
        list[i] *= 2
        sum += list[i]
    print(list)
    return sum

list1 = [1,2,3,4,5,6,7,8,9]
#sum = iterateAndReturn(list)
#print(sum)

#map
newList = list(map(lambda n: n*3, list1))
print(newList)

#filter 
filteredList = list(filter(lambda n: n%2==0, list1))
print(filteredList)

print(bool(14), bool(), bool(1+2), bool(0))
#for x in [0, 1, 2]: 
 #   for y in [0, 1, 2, 3, 4, 5]: print('yes')

x = 10 
y = 5 
result = x // y + x % y 
print(result)