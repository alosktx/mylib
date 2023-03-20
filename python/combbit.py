# info: 实现将位按序进行组合的功能
# run: python3 combbit.py
class combbit:
    def comb_seq(self, num):
        sum = 0
        for n in num: sum =(sum << 1) | n
        return sum
    def comb_bit(self, *num):
        sum = 0
        for n in num: sum =(sum << 1) | n
        return sum

# test
a = combbit()
list_t = [1,0,0,1,1,1,0,0,1,0,0,0,1,1,0]
tuple_t = (1,0,0,1,1,1,0,0,1,0,0,0,1,1,0)
print(bin(a.comb_seq(list_t)))
print(bin(a.comb_seq(tuple_t)))
print(bin(a.comb_bit(1,0,0,0,0,0,1,0,1,1,1,0,1,1,1,0)))
