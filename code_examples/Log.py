## 将print内容写入`.txt`文件
### 方法一

import os
t = 5
s = 'hello world!'
with open('test.txt','a') as file0:
    print('%d' % t,'%s' % s,file=file0)

### 方法二

import sys
import os
 
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass
 
 
path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('a.txt')
print(path)
print(os.path.dirname(__file__))
print('------------------')
for i in range(5, 10):
    print("this is the %d times" % i)


### 方法三

# python<你的python文件.py>outputfile.txt

