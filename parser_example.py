'''
author: 谢韬
该文件是一个词法分析文件，接受一个格式化的字符串，生成一系列的指令
'''

from node import *
from utility.parse_latex import *

#前置特殊字符串ObjIns
#例如一个变量x在这里会变成ObjIns_x
str_spec = "ObjIns_"

#提供了将一个symbol列表中的若干项转换成一个供exec使用的字符串
def symbols2str(command, start_index, cnt, str_spec = ""):
    ret = ""
    for i in range(cnt):
        if ret == "":
            ret = ret + str_spec + command[start_index + i]
        else:
            ret = ret + ", " + str_spec + command[start_index + i]
    return "[" + ret + "]"

def generateCommands(command_list, graph):
    #command_list：一个list包含若干字符串，表示输入的集合
    #返回值：一个list，顺序exec执行即可
    ret = []
    res = []
    cnt = 0
    has_error = False
    error_list = []
    global str_spec
    for command_line in command_list:
        command = None
        if command_line.startswith("Constraint"):
            command = [command_line]
        else:
            command = command_line.split(" ")
        NodeType = command[0]
        #当输入为一个约束表达式时，直接将约束表达式字符串扔到constraints列表中
        if NodeType.startswith("#"):
            continue
        if NodeType.startswith("Constraint"):
            ret.append("constraints.append('%s')" % command[0][11:len(command[0])])
        #当输入为一个求解请求时，将求解请求的变量扔到返回的res列表中
        elif NodeType == "Query":
            res = res + command[1:]
        #当输入为一个节点定义时，根据节点的不同类型做不同处理
        elif NodeType in graph.nodes.keys():
            node = graph.nodes[NodeType]
            #如果是对象节点，则新建一个symbol和一个ObjectInstance
            if isinstance(node, ObjectNode):
                ret.append("%s = Symbol('%s')" % (command[1], command[1]))
                ret.append("%s%s = ObjectInstance(graph.%s, '%s%s')" % (str_spec, command[1], command[0], str_spec, command[1]))
                ret.append("symbol2ins['%s'] = %s%s" % (command[1], str_spec, command[1]))
                ret.append("obj_instances['%s'] = %s%s" % (command[1], str_spec, command[1]))
            #如果是操作节点，则新建一个操作节点连接给出的若干对象节点
            elif isinstance(node, OperationNode):
                input = symbols2str(command, 1, len(node.input), str_spec=str_spec)
                output = symbols2str(command, 1 + len(node.input), len(node.output), str_spec=str_spec)
                ret.append("%s = graph.OperationInstance(graph.%s, %s, %s)" % (command[0] + str(cnt), command[0], input, output))
                ret.append("op_instances.append(%s)" % (command[0] + str(cnt)))
                cnt = cnt + 1
            #如果是约束节点，则新建一个约束节点连接给出的若干对象节点
            elif isinstance(node, ConstraintNode):
                input = symbols2str(command, 1, len(node.input), str_spec=str_spec)
                ret.append("%s = graph.ConstraintInstance(graph.%s, %s)" % (command[0] + str(cnt), command[0], input))
                ret.append("op_instances.append(%s)" % (command[0] + str(cnt)))
                cnt = cnt + 1
        elif NodeType == "":
            pass
        else:
            has_error = True
            error_list.append("未能编译的指令: %s" % command_line)
    return {"cmd": ret, "res": res, "has_error": has_error, "error_list": error_list}









