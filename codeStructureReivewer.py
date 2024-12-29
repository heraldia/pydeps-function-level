#target_dir = '/Users/y0f00k5/Documents/w/SCPH/scph-forecaster/src/'
#target_dir = '/Users/y0f00k5/Documents/w/topK/driving-distance-Repos/DrivingDistanceAzureML/src/DriveDistance'
#target_dir = '/Users/y0f00k5/Documents/w/ReqHelper/Hiring-Prompt-To-Hire/data_science/'
#target_dir = '/Users/y0f00k5/Documents/w/CallRouting/people-ai-airflow'
target_dir = '/Users/y0f00k5/Documents/w/CallRouting/genai'

Flag_analyze_a_certain_script = True
Flag_analyze_a_certain_script = False
filename_of_this_certain_script = 'utils.py'

import os
import sys
from collections import defaultdict
import graphviz  # doctest: +NO_EXE
import re
import pysnooper

function_set = set()
class_set = set()

def traverFilesInFolder(target_dir):
    # get all classNames and functionNames
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for fn in files:
            if not fn.endswith('.py') or 'deleted_' in fn:
                continue
            #print (os.path.join(root,fn))

            # Analyze a certain script !!!!!
            if Flag_analyze_a_certain_script and filename_of_this_certain_script not in os.path.join(root,fn):
                continue

            with open(os.path.join(root,fn), 'r', encoding='utf-8') as f:
                try:
                    for row in f:
                        #print(sys._getframe().f_lineno,'| row: ',row  ); import pdb;pdb.set_trace() # 2022_0506_1927 

                        row = str(row).encode('utf-8').strip().decode('utf-8')

                        if re.match("\s*def", row) or re.match("\s*class", row):
                            if 'class' in row:
                                t = row.replace('class ','').rstrip(":").strip()
                                #class_set.add(os.path.join(root,fn)+":"+t)
                                class_set.add(t)
                            else:
                                t = row.replace('def ','').strip()
                                i = t.find('(') 

                                function_set.add(os.path.join(root,fn).replace(target_dir, "")+"-"+t[:i])
                except Exception as e:
                    print(52, e)


    print('class_set | ', class_set) # 2022_0413_1125
    print('function_set | ', function_set) # 2022_0413_1125

    # search calls for each className and functionName
    function_callable_dic = defaultdict(list)
    flag_in_comment_block = False


    for root, dirs, files in os.walk(target_dir, topdown=False):
        for fn in files:

            if not fn.endswith('.py') and not fn.endswith('.ipynb'):
                continue

            if fn.endswith('.py'):
                cur_class_name = 'None'
                cur_function_name = fn
            if fn.endswith('.ipynb'):
                cur_class_name = 'None'
                cur_function_name = fn

            #print (os.path.join(root,fn))

            with open(os.path.join(root,fn), 'r') as f:
                flag_in_comment_block = False
                for row in f:
                    if re.search( "\s{4,}#",row) or row.startswith("#"): 
                        continue
                    if not flag_in_comment_block and row.startswith('"""'): 
                        flag_in_comment_block = True
                    elif flag_in_comment_block and row.startswith('"""'): 
                        flag_in_comment_block = False

                    if flag_in_comment_block:
                        continue

                    class_definition = False
                    method_definition = False

                    if re.match("\s*def", row) or re.match("\s*class" , row):
                        if 'class' in row:
                            cur_class_name = row.replace('class ','').rstrip(":").strip()
                            cur_function_name = 'None'
                            class_definition = True
                            method_definition = False
                        else:
                            t = row.replace('def ','').strip()
                            i = t.find('(') 
                            cur_function_name = os.path.join(root,fn).replace(target_dir,"") + '-' + str(t[:i])
                            method_definition = True
                            class_definition = False
                            #cur_function_name = str(t[:i])
                            #cur_function_name = fn+"-"+str(t[:i])

                    if method_definition:
                        continue

                    if '(' not in row:
                        continue
                        
                    for _func in function_set:
                        func = _func[_func.find('-')+1:]
                        for func in [func+'(', func+',', func+' (', func+' ,']:
                            if func in row:
                                function_callable_dic.setdefault(cur_function_name, []).append(_func)

    print(sys._getframe().f_lineno,'| function_callable_dic', function_callable_dic) # 2022_0413_1210

    return function_callable_dic


def render_function_callable_dic(function_callable_dic):

    edge_set = set()
    dot = graphviz.Digraph(comment=f'function calls: {target_dir}')

    for k in function_callable_dic:
        if 'root' in k or 'None' in k:
            continue

        if k.endswith('.py'):
            dot.attr('node', shape='doublecircle')
        elif k.endswith('.ipynb'):
            dot.attr('node', shape='rectangle') 
        else:
            dot.attr('node', shape='') 

        dot.node(k)

        dot.attr('node', shape='') 
        for v in function_callable_dic[k]:
            if (k,v) in edge_set:
                continue
            dot.node(v)
            dot.edge(k, v)
            edge_set.add((k,v))

    dot.render('./function-call.gv').replace('\\', '/')


if __name__ == '__main__':
    if not target_dir.endswith('/'):
        target_dir += '/'
    function_callable_dic = traverFilesInFolder(target_dir)
    render_function_callable_dic(function_callable_dic)

