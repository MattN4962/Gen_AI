"""
list = ['matt', 'sara', 'quinton', 'olivia']
#print(list[-1])

contains = 'matt' in list
#print(len(list))

for n in list:
    for i in n:
        print(i)


name = input("Enter a name")
age = int(input("What's their age"))

if(age > 20):
    print("Have a drink")
else:
    print("Go home")


cities = ["PGH", "CHI", "NY", "LA", "HOU"]

name = input("Enter your name: ")
age = int(input("Enter your age : "))
city = input("Enter your city abbreviation: ")

if city in cities and age > 30:
    print("Welcome to the conference")
else:
    print("Error")


names = ['john','marie','amanda','peter','yurie']
for name in names:
    if len(name) > 5:
        print(name)


hidden_num = 30
count = 0
for count in range(3):
    guess = int(input("Guess a number: "))
    if guess == hidden_num and count < 2:
        print("You win")
        break
    elif guess > hidden_num and count < 2:
        print("lower")        
    elif guess < hidden_num and count < 2:
        print("higher")
    else:
        print("Exceeded guesses")


List of services
Customer requests for a service 
Is the service supported and what is the highest category of requests

        
list = []
_range = range(0, 10, 1)

for i in _range:
    list.append(i)

print(list)
"""
newList = [(2,1), (3,5), (4,9)]
element = newList[0]
x,y = element
print(x,y)
print(element)
key = element[0]
value = element[1]
print(key, value)


       

    

