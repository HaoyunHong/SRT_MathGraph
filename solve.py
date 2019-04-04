from node import *
from parser_example import *
#输入一个问题字符串列表和一个图谱文件，返回结果
#问题字符串列表：["Complex z", "Constraint z**2+1", "Query z.area"]
def q_solve(question_input_list, graph_file, printTemp=False):
    print_tab = "  "

    graph = __import__(graph_file)
    obj_instances = {}
    op_instances = []
    con_instances = []
    commands = generateCommands([command_str.strip() for command_str in question_input_list], graph)

    #如果parse指令出错则返回错误信息
    if commands["has_error"]:
        return commands["error_list"]
    if printTemp:
        print("初始化指令列表")
        for command in commands["cmd"]:
            print(print_tab, command)

    symbol2ins = {}
    symbol2sympy = {}
    constraints = []
    constraints_judge = []
    basic_symbols = []

    #根据节点描述指令生成对象
    for command in commands["cmd"]:
        exec(command)
    #生成symbol2sympy
    for symbol in symbol2ins:
        symbol2sympy[symbol] = symbol2ins[symbol].toSympyInstance()
    for i in range(len(constraints)):
        constraints[i] = eval(constraints[i]).subs(symbol2sympy)
    if printTemp:
        print("直接约束集合")
        for i in range(len(constraints)):
            print(print_tab, constraints[i])
    #加入节点约束
    for name in obj_instances:
        constraints = constraints + obj_instances[name].getEquationSet()
    for instance in op_instances:
        constraints = constraints + instance.getEquationSet()
    for instance in con_instances:
        constraints = constraints + instance.getEquationSet()
    if printTemp:
        print("所有约束集合")
        for i in range(len(constraints)):
            print(print_tab, constraints[i])
    #计算所有未知量
    for name in obj_instances:
        basic_symbols = basic_symbols + obj_instances[name].getSymbols()
    if printTemp:
        print("未知量")
        print(print_tab, basic_symbols)
    #求解所有未知量
    results = solve(constraints, basic_symbols, dict=True)
    #求所要的结果
    result_cnt = 0
    ret = []
    for result in results:
        #判断结果是否满足条件
        judge = True
        for name in obj_instances:
            judge = judge and obj_instances[name].judgeResult(result)
        for ins in con_instances:
            judge = judge and ins.judgeResult(result)
        obj_PV = {}
        for name in obj_instances:
            if obj_instances[name].objNode.isSympyInstance():
                obj_PV[name] = obj_instances[name].toSympyInstance().subs(result)
        for constraint in constraints_judge:
            judge = judge and eval(constraint, obj_PV)
        if not judge:
            continue
        ret.append({})
        for name in commands["res"]:
            #加入结果集
            if name.count(".") == 0:
                #对应普通的求值
                ret[result_cnt][name] = symbol2ins[name].toSympyInstance().subs(result)
            else:
                #对应求特殊属性或者基本属性
                temp_l = name.split(".")
                if temp_l[1] in symbol2ins[temp_l[0]].PV.keys():
                    #对应求基本属性
                    ret[result_cnt][name] = symbol2ins[temp_l[0]][temp_l[1]].subs(result)
                else:
                    #对应求特殊属性
                    ret[result_cnt][name] = symbol2ins[temp_l[0]].getSpecialAttr(temp_l[1], result)
        result_cnt = result_cnt + 1
    #打印结果
    if printTemp:
        for ret_index in range(len(ret)):
            print("结果", ret_index, ":")
            for name in ret[ret_index]:
                print(print_tab, name, ":", ret[ret_index][name])
    return ret


