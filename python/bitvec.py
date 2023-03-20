# info: 提供一个类似 verilog 语言中可对信号值（整数）进行提位： signal[x]; 截取： signal[y:x]; 赋值： signal[x] = a; signal[y:x] =b; 组合: signal = {signal[x], signal[y:x]} 等功能
# run: python3 bitvec.py
# import sys
# 前提条件: python3 中int是无限大的（有无限多位）
# print(((1 << 100000)))

#int: get_bit, get_slice, set_bit, set_slice, delete_bit, delete_slice, insert_bit, insert_slice, reverse_bit(reverse_all), reverse_slice, reverse_highbit, re_order_bit
class bitv(int):
    def getb(self, index): 
        return bitv((self >> index) & 1)   
    def gets(self, start, end):
        width = start - end + 1
        return bitv((self >> end) & ((1 << width) - 1))
    # index >= 0 ，value = 1 or 0
    def setb(self, index, value):
        assert(index >= 0)
        if(value == 1):
            print(bin(1<<index))
            return bitv(((1<<index) | self))
        elif(value == 0):
            highbit = (self >> (index + 1)) << (index + 1) 
            lowbith = self & ((1 << (index + 1)) - 1)
            lowbitn = ((1<<index)-1) & lowbith 
            print(bin(highbit), bin(lowbith), bin(lowbitn)) #debug
            return bitv(highbit | lowbitn)
        else:
            print("[setb]: value is not 1 or 0")
            return bitv(self)  
    # start > end >= 0 当value的位数多于 width时，会截取为width位， 当value位数不足width时，会value高位填0补充为width位， 总之最后改变的位数就是width位  
    def sets(self, start, end, value):
        assert(start > end)
        assert(end >= 0)
        width = start - end + 1
        val = (value &  ((1 << width) - 1)) << end
        highbit = (self >> (start + 1)) << (start + 1) 
        lowbit = self & ((1 << end) - 1)
        print(bin(highbit), bin(val), bin (lowbit)) #debug
        return bitv(highbit | val | lowbit)
    # index >= 0
    def delb(self, index):
        assert(index >= 0)
        highbit = (self >> (index + 1)) << index
        lowbit = self & ((1 << index) - 1)
        print(bin(highbit), bin(lowbit)) #debug
        return bitv(highbit | lowbit )
    # start > end >= 0 
    def dels(self, start, end):
        assert(start > end)
        assert(end >= 0)
        highbit = ((self >> (start + 1)) << end)
        lowbit = (self & ((1 << end) - 1))
        print(bin(highbit), bin(lowbit)) #debug
        return bitv(highbit| lowbit)
    # index >= 0 ，value = 1 or 0
    def inb(self, index, value):
        assert(index >= 0)
        highbit = (self >> index) << (index + 1) 
        lowbit = self & ((1 << index) - 1)
        print(bin(highbit), bin(lowbit)) #debug
        if(value == 0):
            return bitv(highbit | lowbit)
        elif(value == 1):
            return bitv(highbit | (1<<index) | lowbit)
        else:
            print("[inb]: value is not 1 or 0")
            return bitv(self) 
    # start > end >= 0 当value的位数多于 width时，会截取为width位， 当value位数不足width时，会value高位填0补充为width位， 总之最后插入的位数就是width位
    def ins(self, start, end, value): 
        assert(start > end)
        assert(end >= 0)
        width = start - end + 1
        val = (value &  ((1 << width) - 1)) << end
        highbit = (self >> end) << (start + 1) 
        lowbit = self & ((1 << (end)) - 1)
        print(bin(highbit), bin(val), bin (lowbit)) #debug
        return bitv(highbit | val | lowbit)
    # index >= -1
    def revb(self, index):
        assert(index >= -1)
        if(index == -1): #取反从左边第一位1开始的所有位
            length = self.bit_length()
            bit_allr = ((1 << length) - 1) - self
            print(bin((1 << length) - 1)) #debug
            return bitv(bit_allr)
        else:
            highbit = (self >> (index + 1)) << (index + 1) 
            lowbit = self & ((1<<index) - 1)
            the_bit = (self >> index) & 1
            the_bitr = 1 - the_bit
            print(bin(highbit),bin(lowbit),bin(the_bit),bin(the_bitr)) #debug
            return bitv(highbit | (the_bitr << index) | lowbit)
    # start > end >= 0 
    def revs(self, start ,end):
        assert(start > end)
        assert(end >= 0)
        width = start - end + 1
        highbit = (self >> (start + 1)) << (start + 1) 
        lowbit = self & ((1 << end) - 1)
        the_bits = (self >> end) & ((1 << width ) - 1) 
        the_bitsr = ((1 << width) - 1) - the_bits
        print(bin(highbit), bin(lowbit), bin(the_bits), bin(the_bitsr)) #debug
        return bitv(highbit | (the_bitsr << end) | lowbit)
    def revhigh(self):
        length = self.bit_length()
        bit_revh = self & ((1<<(length - 1)) - 1)   
        return bitv(bit_revh)
    def reorder(self):
        length = self.bit_length()
        bit_reorder = 0
        for i in range(length):
            one_bit = (self >> i) & 1
            bit_reorder = (bit_reorder << 1) | one_bit
        print(length, bin(bit_reorder)) #debug
        return bitv(bit_reorder)
    #重载操作符 []
    def __getitem__(self, index):
        return self.getb(index)  

# 实际上一个数通过高位填0，其最高位可以是无限的，以下测试注释中所说的高位边界是指最左边为1的那一位, 而由于高位可以无限延长，所以以下对高位边界的测试实质上与对中间位的测试无异


# test bitv.setb() DebugInfo: self (1<<index) & highbit lowbith lowbitn
a = bitv(0b1101101111001101)  
# 1101101111001101 self
#            10000 [4]  
assert (a.setb(4,1) == 0b1101101111011101) #中间位设为1
# 1101101111000000 [ :4] 
#             1101 [3:0]
#              101 0[2:0]
assert (a.setb(3,0) == 0b1101101111000101) #中间位设为0
# 1101101111001101 self
#                1 [0]  
assert (a.setb(0,1) == 0b1101101111001101) #低位边界设为1
# 1101101111001100 [ :1]
#                1 [0]
#                0  0
assert (a.setb(0,0) == 0b1101101111001100) #低位边界设为0
# 1101101111001101 self
# 1000000000000000 [15]
assert (a.setb(15,1) == 0b1101101111001101) #高位边界设为1
# 0                [ :16]
# 1101101111001101 [15:0]
#  101101111001101 0[14:0]
assert (a.setb(15,0) == 0b0101101111001101) #高位边界设为0
#   1101101111001101 self
# 100000000000000000 [17]
assert (a.setb(17,1) == 0b101101101111001101) #超出高位边界设1
# 0                [NAL]
# 1101101111001101 [16:0]
# 1101101111001101 [16:0]
assert (a.setb(17,0) == 0b001101101111001101) #超出高位边界设0


# test bitv.sets() DebugInfo: highbit value lowbit
a = bitv(0b1101101111001101)    
# 1101101111000000 [ :6]
#           110000 [5:3]
#              101 [2:0]
assert (a.sets(5,3,0b110) == 0b1101101111110101) #中间位修改
# 1101101110000000 [ :7]
#           110000 [6:3]
#              101 [2:0]
assert (a.sets(6,3,0b110) == 0b1101101110110101) #中间位修改， 测试高位补0
# 1101101111000000 [ :6]
#           110000 [5:3]
#              101 [2:0]
assert (a.sets(5,3,0b1011110) == 0b1101101111110101) #中间位修改， 测试截取
# 1101101111000000 [ :4]
#               10 [3:0]
#                0 [NAL] 0 进行 '或' 运算不影响原值
assert (a.sets(3,0,0b0010) == 0b1101101111000010) #低位边界修改
# 0              [NAL]
# 10000000000000 [15:13]
#  1101111001101 [12:0]
assert (a.sets(15,13,0b001) == 0b11101111001101) #高位边界修改
# 0                  [NAL]
# 110000000000000000 [17:14]
#      1101111001101 [13:0]
assert (a.sets(17,14,0b1100) == 0b110001101111001101) #跨越高位边界修改
# 0                   [NAL]
# 1110000000000000000 [18:16]
#    1101101111001101 [15:0]
assert (a.sets(18,16,0b111) == 0b1111101101111001101) #超过高位边界(但相邻)修改
# 0                     [NAL] 
# 111000000000000000000 [20:18]
#      1101101111001101 [15:0]
assert (a.sets(20,18,0b111) == 0b111001101101111001101) #超过高位边界(但相邻)修改


# test bitv.delb() DebugInfo: self highbit lowbit
a = bitv(0b1101101111001101)    
# 1101101111001101 self
# 110110111100100  [ :3]
#               1  [1:0] 
assert (a.delb(2) == 0b110110111100101) # 删除中间位
# 1101101111001101 self
# 110110111100110  [ :1]
#               0  [NAL]
assert (a.delb(0) == 0b110110111100110) # 删除低位边界
# 1101101111001101 self
# 0                [ :16]
#  101101111001101 [14:0]
assert (a.delb(15) == 0b101101111001101) # 删除高位边界
# 1101101111001101 self
# 0                [ :17]
# 1101101111001101 [15:0]
assert (a.delb(16) == 0b1101101111001101) # 删除超出高位边界

# test bitv.dels() DebugInfo: self highbit lowbit
a = bitv(0b1101101111001101)    
# 1101101111001101 self
# 1101101111000    [:4]
#             1    [0]
assert (a.dels(3,1) == 0b1101101111001) #删除中间位
# 1101101111001101 self
# 11011010000000   [:9]
#        1001101   [6:0]
assert (a.dels(8,7) == 0b11011011001101) #删除中间位
# 1101101111001101  self
# 1101101111001     [ :3]
#             0     [NAL]
assert (a.dels(2,0) == 0b1101101111001) #删除低边界位
#  1101101111001101 self
# 0                 [ :16]
#     1101111001101 [12:0]
assert (a.dels(15,13) == 0b1101111001101) #删除高边界位
#   1101101111001101 self
# 0                  [ :18]
#       101111001101 [11:0]
assert (a.dels(17,12) == 0b101111001101) #跨越高位边界删除
#   1101101111001101 self
# 0                  [ :18]
#   1101101111001101 [15:0]
assert (a.dels(17,16) == 0b1101101111001101) #超出高位边界删除
    

# test bitv.ins() DebugInfo: highbit value lowbit 
a = bitv(0b1101101111001101)    
# 11011011110010000000 [ :7]==[ :3] 高位到7位等于原来的高位到3位
#               110000 [6:3]
#                  101 [2:0]
assert (a.ins(6,3,0b110) == 0b11011011110010110101) #中间插入，测试高位补0
# 110110111100100000 [ :5]==[ :3]
#              11000 [4:3]
#                101 [2:0]
assert (a.ins(4,3,0b111) == 0b110110111100111101) #中间插入，测试截取
# 1101101111001101000 [ :3]==[:0]
#                 111 [2:0] 
#                   0 [NAL] 
assert (a.ins(2,0,0b111) == 0b1101101111001101111) #低位边界插入
# 1000000000000000000 [18] == [15]
#  101000000000000000 [17:15]
#     101101111001101 [14:0]
assert(a.ins(17,15,0b101) == 0b1101101101111001101) #高位边界插入
# 0                    [NAL] 
# 10100000000000000000 [19:17]
#     1101101111001101 [15:0] 
assert (a.ins(19,17,0b101) == 0b10101101101111001101) #高于高位边界插入
# 0                   [NAL]
# 1010000000000000000 [18:16]
#    1101101111001101 [15:0]
assert (a.ins(18,16,0b101) == 0b1011101101111001101) #高于高位边界（但相邻）插入
# 110000000000000000000 [20:18] == [15:13]
#    110110000000000000 [17:13]
#         1101111001101 [12:0]
assert (a.ins(17,13,0b11011) == 0b110110111101111001101) #跨越高位边界插入


# test bitv.inb() DebugInfo: highbit lowbit 
a = bitv(0b1101101111001101)   
# 11011011110010000 [ :4] = [ :3]
#               101 [2:0] 
assert (a.inb(3,1) == 0b11011011110011101) #中间插入1
assert (a.inb(3,0) == 0b11011011110010101) #中间插入0
# 11011011110011010 [ :1] = [ :0]
#                 0 [NAL]
assert (a.inb(0,1) == 0b11011011110011011) #低位边界插入1
assert (a.inb(0,0) == 0b11011011110011010) #低位边界插入0
# 10000000000000000 [16] == [15]
#   101101111001101 [14:0]
assert (a.inb(15,1) == 0b11101101111001101) #高位边界插入1
assert (a.inb(15,0) == 0b10101101111001101) #高位边界插入0
# 0                [NAL]
# 1101101111001101 [15:0]
assert(a.inb(17,1) == 0b101101101111001101) #高位以上插入1
assert(a.inb(17,0) == 0b001101101111001101) #高位以上插入0
# 0                [NAL]
# 1101101111001101 [15:0]
assert(a.inb(16,1) == 0b11101101111001101) #高位以上相邻位插入1
assert(a.inb(16,0) == 0b01101101111001101) #高位以上相邻位插入0

# test bitv.revb() DebugInfo: highbit lowbit the_bit the_bitr | 
a = bitv(0b1101101111001101)   
# 1101101111001100 [ :1]
#                0 [NAL]
#                1 [0]
#                0 [0]~
assert(a.revb(0) == 0b1101101111001100) #低位边界翻转
# 1101101111001000 [ :3]
#                1 [NAL] 
#              1   [2] 
#              0   [2]~
assert(a.revb(2) == 0b1101101111001001) #中间位翻转
# 0                  [ :16]
#   101101111001101   [14:0]
#  1                  [15]
#  0                  [15]~
assert(a.revb(15) == 0b0101101111001101) #高位边界翻转
# 0                    [ :18]
#    01101101111001101 [16:0]
#   0                  [17]
#   1                  [17]~
assert(a.revb(17) == 0b101101101111001101) #高于高位边界翻转
# 1111111111111111 
assert (a.revb(-1) == 0b0010010000110010)                          


# test.bitv.revs() DebugInfo: 
a = bitv(0b1101101111001101)   
# 1101101111001100   [ :2]
#                 0  [NAL] 
#                1   [1:0]
#               10   [1:0]~
assert(a.revs(1,0) == 0b1101101111001110) #低位边界翻转
# 1101101111000000 [ :6]
#              101 [2:0] 
#             1    [5:3]
#           110    [5:3]~
assert(a.revs(5,3) == 0b1101101111110101) #中间位翻转
# 0                 [ :16]
#     1101111001101 [12:0]
#  110              [15:13]
#    1              [15:13]~
assert(a.revs(15,13) == 0b0011101111001101) #高位边界翻转
# 0                    [ :18]
#        1101111001101 [12:0] 
#     110              [17:13]  
#   11001              [17:13]~  
assert(a.revs(17,13) == 0b110011101111001101) #跨越高位边界翻转
# 0                    [ :18]
#    1101101111001101  [15:0]
#   0                  [17:16]
#  11                  [17:16]~
assert(a.revs(17,16) == 0b111101101111001101) #高于高位边界翻转

# test.bit.revhigh()
a = bitv(0b1101101111001101)   
assert (a.revhigh() == 0b101101111001101)

# test.bit.revhigh()
a = bitv(0b1101101111001101)   
assert (a.reorder() == 0b1011001111011011)