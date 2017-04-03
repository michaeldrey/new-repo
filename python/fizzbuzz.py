

for n in range(0, 101):
    if n % 3 == 0 and n % 5 == 0:
        print str(n) + " - Fizzbuzz"
        #n += 1
    elif n % 3 == 0:
        print str(n) + " - Fizz"
        #n += 1
    elif n % 5 == 0:
        print str(n) + " - Buzz"
        #n += 1
    else:
        print n
        #n += 1
