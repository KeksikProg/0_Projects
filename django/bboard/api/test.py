num = int(input())

def magic(num):
    suma = 0
    for i in range(1, num + 1):
        if num % i == 0:
            suma += i
    print(suma)

magic(num)