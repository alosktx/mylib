## c
## cpp
## python
- bitvec.py
    - 提供一个类似 verilog 语言中可对信号值（整数）进行提位： signal[x]; 截取： signal[y:x]; 赋值： signal[x] = a; signal[y:x] =b; 组合: signal = {signal[x], signal[y:x]} 等功能       
- combbit.py
    - 实现将位按序进行组合的功能
- cutstr.py
    - 将字符串分隔成多段，每段长 each_num, 返回一个列表