import sys
import os
import re
from jinja2 import Environment, FileSystemLoader

def extract_kernel_code(file_path, kernel_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 建立正則表達式來擷取對應 kernel 的 lambda 函數
    pattern = rf'Kernel\(\s*"{re.escape(kernel_name)}".*?\{{(.*?)\}}\s*\)\s*,'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(0).strip()
    else:
        return None

class NativeKernelsCppCodegen:
    def code_gen(self, NativeKernels_cpp_file, template_file, executionPlan_Obj):
        kernel_list = []
        kernel_codes = []
        quantized_code_path = os.path.join('kernels', 'quantized','RegisterCodegenUnboxedKernelsEverything.cpp')
        portable_code_path = os.path.join('kernels', 'poartable','RegisterCodegenUnboxedKernelsEverything.cpp')

        for i in range(len(executionPlan_Obj)):
            operatorsObj = executionPlan_Obj[i]['operators']
            num_operators = len(operatorsObj)
            for j in range(num_operators):
                kernel_list.append(operatorsObj[j]['name'] + '.' + operatorsObj[j]['overload'])

        for i in range(len(kernel_list)):
            prefix = kernel_list[i].split('::')[0]
            if prefix == 'quantized_decomposed':
                kernel_code = extract_kernel_code(quantized_code_path, kernel_list[i])
            else:
                kernel_code = extract_kernel_code(portable_code_path, kernel_list[i])

            if kernel_code:
                kernel_codes.append(kernel_code)
            else:
                print(f"unable find kernel {kernel_list[i]}")

        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        output = template.render(kernel_codes = kernel_codes)
        NativeKernels_cpp_file.write(output)
