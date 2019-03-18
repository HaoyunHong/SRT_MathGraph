from node2 import *
from sympy import *

#声明一个数学图谱-复数
graph = MathGraph()
#添加实体类-实数
graph.addObjectNode("Real", "x", "im(self['x']) == 0")
#添加实体类-复数
graph.addObjectNode("Complex", "a b", "")
#添加操作类型-获取实部
graph.addOperationNode("GetRealPart", [graph.objNodes["Complex"]], [graph.objNodes["Real"]], "self.output[0]['x'] = re(self.input[0]['a'])")
#添加操作类型-获取虚部
graph.addOperationNode("GetImaginaryPart", [graph.objNodes["Complex"]], [graph.objNodes["Real"]], "self.output[0]['x'] = im(self.input[0]['b'])")
#添加操作类型-计算模长
graph.addOperationNode("CalcMod", [graph.objNodes["Complex"]], [graph.objNodes["Real"]], "self.output[0]['x'] = sqrt(self.input[0]['a']**2 + self.input[0]['b']**2)")
#添加操作类型-复数加法
graph.addOperationNode("ComplexAdd", [graph.objNodes["Complex"], graph.objNodes["Complex"]], [graph.objNodes["Complex"]], "self.output[0]['a'], self.output[0]['b'] = self.input[0]['a']+self.input[1]['a'], self.input[0]['b']+self.input[1]['b']")
#添加操作类型-计算复数乘法
graph.addOperationNode("ComplexMultiply",[graph.objNodes["Complex"],graph.objNodes["Complex"]],[graph.objNodes["Complex"]],"self.output[0]['a'],self.output[0]['b'] = self.input[0]['a']*self.input[1]['a']-self.input[1]['b']*self.input[0]['b'], self.input[0]['a']*self.input[1]['b']+self.input[0]['b']*self.input[1]['a']")
#添加操作类型-计算共轭复数
graph.addOperationNode("GetConjugate", [graph.objNodes["Complex"]], [graph.objNodes["Complex"]], "self.output[0]['a'], self.output[0]['b'] = self.input[0]['a'], -self.input[0]['b']")
#添加约束-相等
graph.addConstraintNode("ComplexEqual", [graph.objNodes["Complex"], graph.objNodes["Complex"]], "self.input[0]['a']==self.input[1]['a'] && self.input[0]['b']== self.input[1]['b']")
#添加约束-共轭
graph.addConstraintNode("ComplexConjugate", [graph.objNodes["Complex"], graph.objNodes["Complex"]], "self.input[0]['a']==self.input[1]['a'] && self.input[0]['b']== -self.input[1]['b']")

'''
#读取现有的数学图谱-复数
graph = loadFile("SimpleComplex.txt")
'''
'''
#声明一个复数实体
compl = ObjectInstance(graph.objNodes["Complex"], "compl", {"a": 3, "b": 4})
#声明一个实数实体
real = ObjectInstance(graph.objNodes["Real"], "real", {"x": 0})
#声明一个操作符将上面两个实体联系起来：计算复数的模长
link = OperationInstance(graph.opNodes["CalcMod"], [compl], [real])
#查看激活运算符前实数值
print(real)
#激活运算符
link.calculate()
#查看激活运算符后实数值
print(real)
#将图谱表示为图像存储在SimpleComplex.pdf中
graph.view("SimpleComplex")
#可以将图谱进行存储
graph.saveFile("SimpleComplex.txt")
'''

list_certain=[]
list_uncertain=[]
list_objinstance=[]
#创建操作数实例
comp1=ObjectInstance(graph.objNodes["Complex"],"compl1",{"a":Symbol('a'),"b":Symbol('b')})
comp2=ObjectInstance(graph.objNodes["Complex"],"compl2",{"a":1,"b":2})
comp3=ObjectInstance(graph.objNodes["Complex"],"compl3",{"a":3,"b":4})
comp_ans=ObjectInstance(graph.objNodes["Complex"],"compl_ans",{"a":0,"b":0})
#创建约束实例
cons1=ConstraintInstance(graph.conNodes["ComplexConjugate"],[comp1,comp3])
#创建操作实例
link=OperationInstance(graph.opNodes["ComplexMultiply"],[comp1,comp2],[comp_ans])
link.calculate()

list_objinstance.append(comp1)
list_objinstance.append(comp2)
list_objinstance.append(comp3)
list_objinstance.append(comp_ans)
for objInstance in list_objinstance:
    if ObjectInstance.isCertain(objInstance):
        list_certain.append(objInstance)
    else:
        list_uncertain.append(objInstance)
#根据不确定实例的属性创建新的所有不确定实例的图谱
graph2=MathGraph()
graph2.addObjectNode("Real", "x", "im(self['x']) == 0")
graph2.addObjectNode("Complex", "a b", "")
graph2.view("contraint")
list_newuncertain=[]
list_name=["real1","real2","real3","real4"]
cnt=0
for objInstance in list_uncertain:
    for keys in objInstance.PV:
        real=ObjectInstance(graph.objNodes["Real"],list_name[cnt],{"x":objInstance.PV[keys]})
        if ~ObjectInstance.isCertain(real):
            list_newuncertain.append(real)
            cnt+=1

for objInstance in list_newuncertain:
    list_uncertain.append(objInstance)

cons1.conNode.C=cons1.conNode.C.split("&&")
a=Symbol('a')
b=Symbol('b')
string1=str(cons1.input[0]['a'])+"-"+str(cons1.input[1]['a'])
string2=str(cons1.input[0]['b'])+"+"+str(cons1.input[1]['b'])
dict_solve=solve([string1,string2],[a,b])
print(dict_solve)
comp1.__setitem__('a',dict_solve[a])
comp1.__setitem__('b',dict_solve[b])

link.calculate()

for i in list_certain:
    print(i,end=' ')
print('\n')
for i in list_uncertain:
    print(i,end=' ')

print(comp_ans)

#networkx







