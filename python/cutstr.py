# info: 将字符串分隔成多段，每段长 each_num, 返回一个列表
# run: python3 cutstr.py 
def cut_str(str_t, each_num):
    return [str_t[i : i + each_num] for i in range(0,len(str_t),each_num)]
#test 
test_str = "78a2b861cc8af82cd45426dc580a4847b7dbe5160bdc0e9f200625b06b2b9dcc00"
print(cut_str(test_str, 8))