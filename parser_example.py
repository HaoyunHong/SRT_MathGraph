'''
author: 谢韬
该文件是一个词法分析文件，接受一个格式化的字符串，生成一系列的指令
'''

from node import *

def generateStrFromStrList(command, start_index, cnt):
    ret = ""
    for i in range(cnt):
        if ret == "":
            ret = ret + command[start_index + i]
        else:
            ret = ret + ", " + command[start_index + i]
    return "[" + ret + "]"

def generateCommands(command_list):
    #command_list：一个list包含若干字符串，表示输入的集合
    #返回值：一个list，顺序exec执行即可
    for i in range(len(command_list)):
        command_list[i] = command_list[i].split(" ")
    ret = []
    res = []
    cnt = 0
    for command in command_list:
        NodeType = command[0]
        if NodeType == "Constraint":
            ret.append("constraints.append('%s')" % command[1])
        elif NodeType == "Query":
            res.append(command[1])
        elif NodeType in nodes.keys():
            node = nodes[NodeType]
            if isinstance(node, ObjectNode):
                ret.append("%s = ObjectInstance(%s, '%s')" % (command[1], node.name, command[1]))
                ret.append("ins_list.append(%s)" % command[1])
            elif isinstance(node, OperationNode):
                input = generateStrFromStrList(command, 1, len(node.input))
                output = generateStrFromStrList(command, 1 + len(node.input), len(node.output))
                ret.append("%s = OperationInstance(%s, %s, %s)" % (command[0] + str(cnt), command[0], input, output))
                ret.append("ins_list.append(%s)" % (command[0] + str(cnt)))
                cnt = cnt + 1
            elif isinstance(node, ConstraintNode):
                input = generateStrFromStrList(command, 1, len(node.input))
                ret.append("%s = ConstraintInstance(%s, %s)" % (command[0] + str(cnt), command[0], input))
                ret.append("ins_list.append(%s)" % (command[0] + str(cnt)))
                cnt = cnt + 1
    return {"cmd": ret, "res": res}









