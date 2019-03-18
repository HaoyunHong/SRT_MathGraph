'''
author: 谢韬
该文件是实例文件，请不要直接修改
'''

from node import *

graph_description = '''
Real = ObjectNode("Real", "x", "", toSympy="self['x']")
Complex = ObjectNode("Complex", "a b", "", toSympy="self['a']+self['b']*I")
GetRePart = OperationNode("GetRePart", [Complex], [Real], "self.output[0]['x']=self.input[0]['a']")
GetImPart = OperationNode("GetImPart", [Complex], [Real], "self.output[0]['x']=self.input[0]['b']")
CalcMod = OperationNode("CalcMod", [Complex], [Real], "self.output[0]['x']=sqrt(self.input[0]['a']**2+self.input[0]['b']**2)")
ComplexConjugate = ConstraintNode("ComplexConjugate", [Complex, Complex], "self.input[0]['a']==self.input[1]['a']&&self.input[0]['b']=-self.input[1]['b']")
'''

exec(graph_description)

def createObjectInstance(objNode, name):
    exec("%s = ObjectInstance(%s, '%s')" % (name, objNode, name), globals())

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















