import sys
import pandas
import os
from jinja2 import Environment, FileSystemLoader

def find_sublist_index(lst, sublst):
    for i in range(len(lst) - len(sublst) + 1):
        if lst[i:i+len(sublst)] == sublst:
            return i
    return -1  # if not found

class MainCCodegen:
    def code_gen(self, main_file, template_file, executionPlan_Obj, backendData_Obj):
        max_scratch_size = 0
        max_rw_buffer_size = 0
        max_input_size = 0

        for e in range(len(executionPlan_Obj)):
            tensorsObj = executionPlan_Obj[e]['values']
            inputsObj = executionPlan_Obj[e]['inputs']
            nonConstBufferSizesObj = executionPlan_Obj[e]['non_const_buffer_sizes']
            for n in range(len(nonConstBufferSizesObj)):
                max_rw_buffer_size = max_rw_buffer_size + nonConstBufferSizesObj[n]

            for i in range(len(inputsObj)):
                inputTensorObj = tensorsObj[inputsObj[i]]
                dim_size = 1
                sizesObj = inputTensorObj['val']['sizes']
                for d in range(len(sizesObj)):
                    dim_size = dim_size * sizesObj[d]
                if inputTensorObj['val']['scalar_type'] == "FLOAT":
                    dim_size = dim_size * 4
                elif inputTensorObj['val']['scalar_type'] == "Int":
                    dim_size = dim_size * 4
                max_input_size = max_input_size + dim_size

        for b in range(len(backendData_Obj)):
            backendDataDataObj = backendData_Obj[b]['data']
            scratch_data_str = "scratch_data"
            scratch_data_list = [ord(char) for char in scratch_data_str]
            scratch_data_offset = find_sublist_index(backendDataDataObj, scratch_data_list)
            scratch_size_offset = scratch_data_offset + 16   #16: Standard block name size
            scratch_size = backendDataDataObj[scratch_size_offset + 3] << 24
            scratch_size = scratch_size + (backendDataDataObj[scratch_size_offset + 2] << 16)
            scratch_size = scratch_size + (backendDataDataObj[scratch_size_offset + 1] << 8)
            scratch_size = scratch_size + (backendDataDataObj[scratch_size_offset + 0])
            print("scratch data size for backend elemnet data {}".format(scratch_size))
            if scratch_size > max_scratch_size:
                max_scratch_size = scratch_size

        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        max_scratch_size = max_scratch_size + 1024
        max_rw_buffer_size = max_rw_buffer_size + 2048
        output = template.render(ethosu_scratch_size = max_scratch_size, input_tensor_size = max_input_size, nonconst_buffer_size = max_rw_buffer_size)
        main_file.write(output)
