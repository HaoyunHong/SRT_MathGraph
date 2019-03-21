'''
author: 谢韬
该文件是示例文件，请不要直接修改
'''

from node import *
from parser_example import *

#graph_description = '''
Real = ObjectNode("Real", "x", "", toSympy="self['x']")
Complex = ObjectNode("Complex", "a b", "", toSympy="self['a']+self['b']*I")
GetRePart = OperationNode("GetRePart", [Complex], [Real], "self.output[0]['x']=self.input[0]['a']", E=["self.output[0]['x']-self.input[0]['a']"])
GetImPart = OperationNode("GetImPart", [Complex], [Real], "self.output[0]['x']=self.input[0]['b']", E=["self.output[0]['x']-self.input[0]['b']"])
CalcMod = OperationNode("CalcMod", [Complex], [Real], "self.output[0]['x']=sqrt(self.input[0]['a']**2+self.input[0]['b']**2)", E=["self.output[0]['x']-sqrt(self.input[0]['a']**2+self.input[0]['b']**2)"])
ComplexConjugate = ConstraintNode("ComplexConjugate", [Complex, Complex], "self.input[0]['a']==self.input[1]['a']&&self.input[0]['b']=-self.input[1]['b']", E=["self.input[0]['a']-self.input[1]['a']", "self.input[0]['b']+self.input[1]['b']"])
#'''

#exec(graph_description)

def createObjectInstance(objNode, name):
    exec("%s = ObjectInstance(%s, '%s')" % (name, objNode, name), globals())
"""
#题目1：
#z1和z2是复数，z1=z2*i，z1+z2=-1+7i，求z1的模长r

#描述：z1和z2是复数，r是实数
createObjectInstance("Complex", "z1")
createObjectInstance("Complex", "z2")
createObjectInstance("Real", "r")
'''
#或者可以使用下面的写法
z1 = ObjectInstance(Complex, "z1")
z2 = ObjectInstance(Complex, "z2")
r = ObjectInstance(Real, "r")
'''

constraints = []
tosolve = []

#描述：z1 = z2 * i
constraints.append("z1 - z2 * I")
#描述：z1 + z2 = -1 + 7i
constraints.append("z1 + z2 + 1 - 7 * I")
#描述：r是z1的模长
#这里也可以自定义函数createOperationInstance，怎么方便怎么来
op = OperationInstance(CalcMod, [z1], [r])
op.calculate()
#描述：求r
#经过op后，r依赖于z1_a和z1_b

#解约束
print("约束集合（包含数学实体）：")
for i in range(0, len(constraints)):
    #替换数学实体为sympy对象
    for name in instances:
        if instances[name].objNode.isSympyInstance():
            constraints[i] = constraints[i].replace(name, name + ".toSympyInstance()")
    print(constraints[i])

print("约束集合（只含基本属性）：")
for i in range(0, len(constraints)):
    constraints[i] = eval(constraints[i])
    print(constraints[i])

for name in instances:
    #搜索所有要解的symbol
    #print(instances[name].getSymbols())
    tosolve = tosolve + (instances[name].getSymbols())
print("所有的基本属性：")
print(tosolve)
res = solve(constraints, tosolve)
print("所有基本属性的解：")
print(res)

for name in instances:
    #将instance中的基本属性替换为解
    instances[name].subs(res)
print("结果：")
print(r['x'])
"""
"""
#题目2：和题目1相同，不过计算方法不同
#这里使用了Instnace的新特性：提取等式约束
#这需要在定义中设置E项
#z1和z2是复数，z1=z2*i，z1+z2=-1+7i，求z1的模长r

#定义解题用列表
ins_list = []
constraints = []
tosolve = []

#以下部分因题而异
#定义z1 z2 r
z1 = ObjectInstance(Complex, "z1")
ins_list.append(z1)
z2 = ObjectInstance(Complex, "z2")
ins_list.append(z2)
r = ObjectInstance(Real, "r")
ins_list.append(r)
#约束：两个等式
constraints.append("z1-z2*I")
constraints.append("z1+z2+1-7*I")
#约束，r是z1的模长
op = OperationInstance(CalcMod, [z1], [r])
ins_list.append(op)

#以下部分不随题目改变而改变
#转化约束：现有约束为题目给出的明文约束，其中包含数学实体
print("约束集合（包含数学实体）：")
for i in range(0, len(constraints)):
    #替换数学实体为sympy对象
    for name in instances:
        if instances[name].objNode.isSympyInstance():
            constraints[i] = constraints[i].replace(name, name + ".toSympyInstance()")
    print(constraints[i])
print("约束集合（只含基本属性）：")
for i in range(0, len(constraints)):
    constraints[i] = eval(constraints[i])
    print(constraints[i])
#完善约束，将诸多节点定义的约束添加到约束集中
for ins in ins_list:
    constraints = constraints + ins.getEquationSet()
print("最终约束集合：")
print(constraints)
#查找所有要解的symbol
for name in instances:
    #搜索所有要解的symbol
    #print(instances[name].getSymbols())
    tosolve = tosolve + (instances[name].getSymbols())
print("所有的基本属性：")
print(tosolve)
results = solve(constraints, tosolve, dict=True)
print("所有基本属性的解：")
print(results)

#解约束，以下部分因题而异（因为最终结果不定）
for result in results:
    for name in instances:
        #将instance中的基本属性替换为解
        instances[name].subs(result)
    print("结果：")
    print(r['x'])
"""
#题目3：和题目1相同，不过计算方法不同
#这里使用了parser中的解析函数，并采用文件作为输入
#z1和z2是复数，z1=z2*i，z1+z2=-1+7i，求z1的模长r

#只需要改变filename或者file中的内容即可
filename = "question_test.txt"
question = [s.strip() for s in open(filename, 'r').readlines()]

#定义解题用列表
ins_list = []
constraints = []
tosolve = []

#直接指令处理
cmds = generateCommands(question)
for cmd in cmds["cmd"]:
    #print(cmd)
    exec(cmd, globals())

#转化约束：现有约束为题目给出的明文约束，其中包含数学实体
print("约束集合（包含数学实体）：")
for i in range(0, len(constraints)):
    #替换数学实体为sympy对象
    for name in instances:
        if instances[name].objNode.isSympyInstance():
            constraints[i] = constraints[i].replace(name, name + ".toSympyInstance()")
    print(constraints[i])
print("约束集合（只含基本属性）：")
for i in range(0, len(constraints)):
    constraints[i] = eval(constraints[i])
    print(constraints[i])
#完善约束，将诸多节点定义的约束添加到约束集中
for ins in ins_list:
    constraints = constraints + ins.getEquationSet()
print("最终约束集合：")
for c in constraints:
    print(c)
#查找所有要解的symbol
for name in instances:
    #搜索所有要解的symbol
    #print(instances[name].getSymbols())
    tosolve = tosolve + (instances[name].getSymbols())
print("所有的基本属性：")
print(tosolve)
results = solve(constraints, tosolve, dict=True)
print("所有基本属性的解：")
print(results)

#解约束，以下部分不随题目变化，因为新版本中将要求的结果写入了题目中
for i in range(len(results)):
    for name in instances:
        #将instance中的基本属性替换为解
        instances[name].subs(results[i])
    print("结果%s：" % str(i + 1))
    for res in cmds["res"]:
        print(res + ": " + str(instances[res].toSympyInstance()))
















