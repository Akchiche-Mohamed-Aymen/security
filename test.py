def calc_power(base, exponent , modulo) :
    res = {
        1 : base % modulo
    }
    for i in range(2, exponent + 1):
        if i % 2 == 0:
            res[i] = (res[i // 2] * res[i // 2]) % modulo
        else:
            res[i] = (res[i - 1] * res[1]) % modulo
    return res[exponent]
print(calc_power(585, 593, 1715)) 