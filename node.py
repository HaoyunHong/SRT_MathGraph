'''
author: 谢韬
请不要修改该文件
'''

from sympy import *

class Node:
    pass

class Instance:
    pass

'''
obj_instances = {}
op_instances = []
con_instances = []
nodes = {}
'''

class ObjectNode(Node):
    def __init__(self, name, P, C, toSympy="", E=[], spec_attr={}):
        #name：指本ObjectNode的名称，例如"Complex"，"Triangle"等
        #P：指对象节点的属性，格式为若干个名称用空格隔开，例如"a b c"
        #C：指对象节点的约束，对某一属性的访问用"self[属性]"表示
        #   例如三角形两边之和大于第三边可以是"self['a']+self['b']>self['c']"
        #toSympy：默认为空字符串，详细可见ObjectInstance类中的toSympyInstance方法
        #E：约束等式的集合，例如三角形有["self['A']+self['B']+self['C']-pi"]等
        #attr: 指特殊属性，例如复数的象限，角度是钝角还是锐角等一些由基本属性所确定的属性
        #      例如复数的象限"area": "1 if ... else 2 if ... else ..."
        #      例如三角形的形状"shape": "'锐角' if $A<pi/2 and $B<pi/2 and $C<pi/2 else '非锐角三角形'"
        #      字典中的key是属性名称，value是一个可以eval的式子
        #      eval中的式子中要使用基本属性则使用$加上基本属性的名称即可，后面会将$替换为某一特定instance的name属性
        self.name = name
        self.P = P.split(" ")
        if self.P.count("") > 0:
            self.P.remove("")
        self.C = C
        self.E = E
        self.toSympy = toSympy
        self.instances = {}
        self.spec_attr = spec_attr

        #global nodes
        #nodes[self.name] = self
        '''
        self.toSave = "ObjectNode\n" + name + "\n" + P + "\n" + C
        '''

    def isSympyInstance(self):
        #判断该对象对应的实体是否可以转化为Sympy对象
        return self.toSympy != ""

class OperationNode(Node):
    def __init__(self, name, input, output, f, E=[]):
        #name：指本OperationNode的名称，例如"CalcMod"等
        #input：一个list，内含若干对象节点，代表输入的类型，例如[Complex]
        #output：一个list，内含若干对象节点，代表输出的类型，例如[Real]
        #f：代表运算规则，其中对输入的访问为"self.input[index][基本属性]"，输出同理
        #   例如复数模长的计算可以是"self.output[0]['x']=sqrt(self.input[0]['a']**2+self.input[0]['b']**2)"
        #E：约束等式的集合，例如复数模长有["self.output[0]['x']-sqrt(self.input[0]['a']**2+self.input[0]['b']**2)"]等
        self.name = name
        self.input = input
        self.output = output
        self.f = f
        self.E = E

        #global nodes
        #nodes[self.name] = self
        '''
        self.instances = []
        self.toSave = "OperationNode\n" + name + "\n"
        cnt = 0
        for objNode in input:
            if cnt != 0:
                self.toSave += " "
            cnt += 1
            self.toSave += objNode.name
        cnt = 0
        self.toSave += "\n"
        for objNode in output:
            if cnt != 0:
                self.toSave += " "
            cnt += 1
            self.toSave += objNode.name
        self.toSave += "\n" + f
        '''

class ConstraintNode(Node):
    def __init__(self, name, input, C, E=[]):
        #name：指本ConstraintNode的名称，例如"ComplexConjugate"等
        #input：一个list，内含若干对象节点，代表输入的类型，例如[Complex, Complex]等
        #C：约束字符串，代表这个点的约束条件，使用self.input[index][基本属性]来对属性进行访问
        #   例如共轭的约束字符串可以是"self.input[0]['a']==self.input[1]['a'] && self.input[0]['b']==-self.input[1]['b']"
        #E：约束等式的集合，例如复数共轭有["self.input[0]['a']-self.input[1]['a']", "self.output[0]['b']+self.output[1]['b']"]等
        self.name = name
        self.input = input
        self.C = C
        self.E = E

        #global nodes
        #nodes[self.name] = self
        '''
        self.instances = []
        self.toSave = "ConstraintNode\n" + name + "\n"
        cnt = 0
        for objNode in input:
            if cnt != 0:
                self.toSave += " "
            cnt += 1
            self.toSave += objNode.name
        self.toSave += "\n" + self.C
        '''

class ObjectInstance(Instance):
    def __init__(self, objNode, name):
        #我们假定每一个数学实体中的基本属性都是一个Sympy的Symbol或者使若干个Symbol组成的表达式
        #基本属性的初始Symbol为该实体的名称+该属性的名称
        self.objNode = objNode
        self.name = name
        self.PV = {}
        for p in self.objNode.P:
            self.PV[p] = Symbol(name + "_" + p, real=True)
        #global obj_instances
        #obj_instances[self.name] = self

    def isCertain(self):
        #每一个Sympy对象中都有一个属性is_number，用来判断该对象是否为一个确定的数
        #当一个数学实体中所有的基本属性都是一个确定的数的时候，该实体也被确定
        certain = True
        for p in self.PV:
            certain = certain and self.PV[p].is_number
            if certain == False:
                break
        return certain

    def isLegal(self):
        #这个函数可能没用？
        #当该实体无法被确定时，默认其为合法
        if self.isCertain() == False:
            return True
        #当该实体被确定时，可以对约束进行计算
        return eval(self.objNode.C)

    def subs(self, PV):
        #PV是一个dict，指将所有基本属性中如果含有PV中的成分则进行替换
        #例如ObjectNode为复数，某一ObjectInstance名称为z，基本属性为a:z_a和b:z_b，PV为{z_a:3}
        #则基本属性变为a:3和b:z_b
        for p in self.PV:
            self.PV[p] = self.PV[p].subs(PV)

    def toSympyInstance(self):
        #将本ObjectInstance转化为一个Sympy实体
        #例如ObjectNode为复数，基本属性为a和b
        #则本函数的返回值为a+b*I
        #toSympy格式为"self['a'] + self['b'] * I"
        return eval(self.objNode.toSympy)

    def toSympyString(self):
        #将toSympy中的self转化为本Instance的name
        return "(" + self.objNode.toSympy.replace("self", self.name) + ")"

    def getSymbols(self):
        #解方程时理论上出现的Symbol应当都是Instance的基础属性，即都有name_attr的命名格式
        #本函数返回了本Instance现在还有的基本属性
        #以复数为例：基本属性为a:3,b:z_b，则本函数返回一个list[z_b]，或者换言之[self['b']]
        #这样的话对所有的Instance进行遍历取symbols就可以得到所有要解方程的变量名
        ret = []
        for p in self.PV:
            if isinstance(self.PV[p], Symbol):
                ret.append(self.PV[p])
        return ret

    def getEquationSet(self):
        ret = []
        for e in self.objNode.E:
            ret.append(eval(e))
        return ret

    def getSpecialAttr(self, attrname, PV):
        PV2 = {}
        for key in PV:
            PV2[str(key)] = PV[key]
        return eval(self.objNode.spec_attr[attrname].replace("$", self.name + "_"), PV2)

    def judgeResult(self, PV):
        PV2 = {}
        for key in PV:
            PV2[str(key)] = PV[key]
        return eval(self.objNode.C, PV2)

    def generateDict(self, PV):
        ret_PV = {}
        for attr in self.PV:
            ret_PV[attr] = self.PV[attr].subs(PV)
        return ret_PV

    def __getitem__(self, item):
        return self.PV[item]

    def __setitem__(self, key, value):
        self.PV[key] = value

class OperationInstance(Instance):
    def __init__(self, opNode, input, output):
        self.opNode = opNode
        self.input = input
        self.output = output
        #global op_instances
        #op_instances.append(self)

    def calculate(self):
        exec(self.opNode.f)

    def getEquationSet(self):
        ret = []
        for e in self.opNode.E:
            ret.append(eval(e))
        return ret

class ConstraintInstance(Instance):
    def __init__(self, conNode, input):
        self.conNode = conNode
        self.input = input
        #global con_instances
        #con_instances.append(self)

    def isLegal(self):
        return eval(self.conNode.C)

    def getEquationSet(self):
        ret = []
        for e in self.conNode.E:
            ret.append(eval(e))
        return ret

    def judgeResult(self, PV):
        input = []
        for i in self.input:
            input.append(i.generateDict(PV))
        return eval(self.conNode.C.replace("self.", ""))






