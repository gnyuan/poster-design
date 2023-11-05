# Author 臧成龙
# coding=utf-8
# @Time    : 2022/5/16 21:09
# @File    : list_to_tree.py
# @Software: PyCharm
# @qq: 939589097

def add_node(p, node):
    # ⼦节点list
    p["children"] = []
    for n in node:
        if n.get("parent_id") == p.get("id"):
            p["children"].append(n)
    # 递归⼦节点，查找⼦节点的节点
    for t in p["children"]:
        if not t.get("children"):
            t["children"] = []
        t["children"].append(add_node(t, node))
    # 退出递归的条件
    if len(p["children"]) == 0:
        p.pop('children')
        p["choice"] = 1
        return


def list_to_route(data):
    root = []
    node = []
    # 初始化数据，获取根节点和其他子节点list
    for d in data:
        d['meta'] = {
            'title': d.pop('title'),
            'ignoreKeepAlive': d.pop('keepalive'),
            'orderNo': d.pop('sort'),
            'hideMenu': d.pop('hide_menu'),
            'icon': d.pop('icon'),
            'fromeSrc': d.pop('from_src'),
        }

        d["choice"] = 0
        if d.get("parent_id") is None:
            root.append(d)
        else:
            node.append(d)
    # print("root----",root)
    # print("node----",node)
    # 查找子节点
    for p in root:
        add_node(p, node)
    # 无子节点
    if len(root) == 0:
        return node

    return root


def list_to_tree(data):
    root = []
    node = []
    # 初始化数据，获取根节点和其他子节点list

    for d in data:
        if d.get('pid') and d.get('pid')!='0': # 数据浏览器转化
            d['parent_id'] = d.get('pid')
        if d.get('cid'): # 数据浏览器转化
            d['id'] = d.get('cid')
        d["choice"] = 0
        if d.get("parent_id") is None:
            root.append(d)
        else:
            node.append(d)
    # print("root----",root)
    # print("node----",node)
    # 查找子节点
    for p in root:
        add_node(p, node)
    # 无子节点
    if len(root) == 0:
        return node

    return root

def list_to_tree_cctong(data):
    root = []
    node = []
    # 初始化数据，获取根节点和其他子节点list

    for d in data:
        # cctong转化
        if d.get('DEPARTMENTID') or d.get('ID'):
            d['id'] = d.get('DEPARTMENTID') or d.get('ID')
        if d.get('PARENTID'):
            d['parent_id'] = d.get('PARENTID')
        d["choice"] = 0
        if d.get("parent_id") == 1:
            root.append(d)
        else:
            node.append(d)
    # print("root----",root)
    # print("node----",node)
    # 查找子节点
    for p in root:
        add_node(p, node)
    # 无子节点
    if len(root) == 0:
        return node

    return root


def aync_list_to_tree_helper(id, mydict, myids, deepLimit):
    if not myids[id]:
        return mydict[id]
    else:
        mydict[id]['children'] = []
        if deepLimit <=0:  # 深度限制，同时，它有children属性
            return mydict[id]
        for i in myids[id]:
            thisdeep = deepLimit -1
            mydict[id]['children'].append(aync_list_to_tree_helper(i, mydict, myids, thisdeep))
        return mydict[id]

def aync_list_to_tree(data, deepLimit=1, parent_id=None):
    '''
    :param data: 数据库中的数据
    :param deepLimit: 限制深度,默认不限制, 一般请求第一层, 即deepLimit=1
    :param parent_id: 限制parent_id,默认不限制，若限制，则取它的子节点
    '''
    mydict  = {d['id']:d for d in data} # 形成对照表
    myids = {d['id']:[] for d in data} # key是id，value是所有子节点的id
    root = []
    for d in data:
        if d['parent_id']:
            myids[d['parent_id']].append(d['id'])
        else:
            root.append(d['id']) 

    ret = []
    if parent_id: # 有具体id，忽略deppLimit参数，返回具体id下的所有子节点
        thisdeep = 100000
        ret.append(aync_list_to_tree_helper(int(parent_id), mydict, myids, thisdeep))
        return ret[0].get('children')
    for r in root:  # 没有具体id，则按层级返回
        thisdeep = int(deepLimit) -1
        ret.append(aync_list_to_tree_helper(r, mydict, myids, thisdeep))
    return ret


