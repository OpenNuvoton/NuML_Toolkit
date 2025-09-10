import os
import json

from generic_codegen.NativeKernels_cpp_codegen import NativeKernelsCppCodegen
from generic_codegen.main_cpp_codegen import MainCCodegen

class GenericCodegen:
    def __init__(self, pte_json, project, **kwargs):
        self.pte_json = pte_json
        self.project = project
        self.extra = kwargs

    @classmethod
    def from_args(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def code_gen(self):
        print('Run generic codegen...')
        print(f"pte_json:{self.pte_json}")
        print(f"project:{self.project}")
        for key, value in self.extra.items():
            print(f"extra param:{key}, {value}")

        template_path = 'generic_codegen'

        jsonFile = open(self.pte_json,'r')
        jsonObj = json.load(jsonFile)
        backendDataObj = jsonObj['backend_delegate_data']
        executionPlanObj = jsonObj['execution_plan']

        #Generate RegisterNativeKernels.cpp file
        NativeKernels_cpp_file_path = os.path.join(self.project, 'RegisterNativeKernels.cpp')
        NativeKernels_cpp_temp_file_path = os.path.join(template_path, 'RegisterNativeKernels_cpp_tmpl.jinja2')
        print(f'RegisterNativeKernels.cpp template path {NativeKernels_cpp_temp_file_path}')
        print(f'RegisterNativeKernels.cpp file path {NativeKernels_cpp_file_path}')

        try:
            NativeKernels_cpp_file = open(NativeKernels_cpp_file_path, "w")
        except OSError:
            print("Could not open NNModel.cpp file")
            return 'unable_generate'

        with NativeKernels_cpp_file:
            NativeKernels_codegen = NativeKernelsCppCodegen()
            NativeKernels_codegen.code_gen(NativeKernels_cpp_file, NativeKernels_cpp_temp_file_path, executionPlanObj)

        #Generate main.cpp file
        main_file_path = os.path.join(self.project, 'main.cpp')
        main_temp_file_path = os.path.join(template_path, 'main_cpp_tmpl.jinja2')
        print(f'template path {main_temp_file_path}')
        print(f'main file path {main_file_path}')

        try:
            main_file = open(main_file_path, "w")
        except OSError:
            print("Could not open main file")
            return 'unable_generate'

        with main_file:
            main_codegen = MainCCodegen()
            main_codegen.code_gen(main_file, main_temp_file_path, executionPlanObj, backendDataObj)

        jsonFile.close()