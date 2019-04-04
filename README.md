# SRT_MathGraph

## 运行环境

**python 3.x**

需要安装sympy包

## 运行指南

在cmd下打开当前目录，执行以下指令即可

```
python graph_example.py
```

以示例题目文件为例，输出应当类似于以下内容

```
题目1:
{'r2': -sqrt(5)}
{'r2': sqrt(5)}
题目2:
{'z1': -sqrt(2)/2 - sqrt(2)*I/2, 'z1.area': '第三象限'}
{'z1': -sqrt(2)/2 + sqrt(2)*I/2, 'z1.area': '第二象限'}
{'z1': sqrt(2)/2 - sqrt(2)*I/2, 'z1.area': '第四象限'}
{'z1': sqrt(2)/2 + sqrt(2)*I/2, 'z1.area': '第一象限'}
题目3:
未能编译的指令: GetRealPart z1 a1
```

## 文件说明（只含有用文件说明）

### node.py

该文件提供了数学图谱的基本节点和数学实体的定义，后续整个图谱的运行都基于本文件

### parser_example.py

提供了一个以结构化字符串列表为输入的函数generateCommands，输出列表编译而成的python代码

### solve.py

提供了q_solve函数，该函数接受一个结构化题目和一个题目类型为输入，输出该题目对应的解

### complex_graph.py

提供了复数相关的数学图谱示例

### graph_example.py

相当于main文件，运行该文件即可

### question_test.txt

数据文件，该文件中存储了需要测试的题目
