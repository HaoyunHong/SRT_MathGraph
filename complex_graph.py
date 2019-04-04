from node import *

#实数
Real = ObjectNode("Real", "x", "", toSympy="self['x']")
#复数
Complex = ObjectNode("Complex", "a b", "", toSympy="self['a']+self['b']*I", spec_attr={"area": "'原点' if $a==0 and $b==0 else '实轴' if $a==0 and $b!=0 else '虚轴' if $a!=0 and $b==0 else '第一象限' if $a>0 and $b>0 else '第二象限' if $a<0 and $b>0 else '第三象限' if $a<0 and $b<0 else '第四象限'", "type": "'普通复数' if $a != 0 and $b != 0 else '实数' if $b == 0 else '纯虚数'"})
#取实部
GetRePart = OperationNode("GetRePart", [Complex], [Real], "self.output[0]['x']=self.input[0]['a']", E=["self.output[0]['x']-self.input[0]['a']"])
#取虚部
GetImPart = OperationNode("GetImPart", [Complex], [Real], "self.output[0]['x']=self.input[0]['b']", E=["self.output[0]['x']-self.input[0]['b']"])
#计算模长
CalcMod = OperationNode("CalcMod", [Complex], [Real], "self.output[0]['x']=sqrt(self.input[0]['a']**2+self.input[0]['b']**2)", E=["self.output[0]['x']-sqrt(self.input[0]['a']**2+self.input[0]['b']**2)"])
#两复数共轭
ComplexConjugate = ConstraintNode("ComplexConjugate", [Complex, Complex], "self.input[0]['a']==self.input[1]['a'] and self.input[0]['b']==-self.input[1]['b']", E=["self.input[0]['a']-self.input[1]['a']", "self.input[0]['b']+self.input[1]['b']"])
#关于虚轴对称
ComplexConjugate2 = ConstraintNode("ComplexConjugate2", [Complex, Complex], "self.input[0]['a']==-self.input[1]['a'] and self.input[0]['b']==self.input[1]['b']", E=["self.input[0]['a']+self.input[1]['a']", "self.input[0]['b']-self.input[1]['b']"])

node_names = ["Real", "Complex", "GetRePart", "GetImPart", "CalcMod", "ComplexConjugate", "ComplexConjugate2"]
nodes = {}
for name in node_names:
    exec("nodes['%s'] = %s" % (name, name))