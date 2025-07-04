import os

from generic_codegen.NNModel_hpp_codegen import NNModelHppCodegen
from generic_codegen.NNModel_cpp_codegen import NNModelCppCodegen
from generic_codegen.main_cpp_codegen import MainCCodegen

class GenericCodegen:
    def __init__(self, model, project, vela_summary, **kwargs):
        self.model = model
        self.project = project
        self.vela_summary = vela_summary
        self.extra = kwargs

    @classmethod
    def from_args(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    
    def code_gen(self):
        print(self.model)
        print(self.project)
        template_path = 'generic_codegen'

        #Generate NNModel.hpp file
        NNModel_hpp_file_path = os.path.join(self.project, 'Model', 'include', 'NNModel.hpp')
        NNModel_hpp_temp_file_path = os.path.join(template_path, 'NNModel_hpp_tmpl.jinja2')
        print(f'NNModel.hpp template path {NNModel_hpp_temp_file_path}')
        print(f'NNModel.hpp file path {NNModel_hpp_file_path}')

        try:
            NNModel_hpp_file = open(NNModel_hpp_file_path, "w")
        except OSError:
            print("Could not open NNModel.hpp file")
            return 'unable_generate'

        with NNModel_hpp_file:
            NNModel_hpp_codegen = NNModelHppCodegen()
            NNModel_hpp_codegen.code_gen(NNModel_hpp_file, NNModel_hpp_temp_file_path, self.model)

        #Generate NNModel.cpp file
        NNModel_cpp_file_path = os.path.join(self.project, 'Model', 'NNModel.cpp')
        NNModel_cpp_temp_file_path = os.path.join(template_path, 'NNModel_cpp_tmpl.jinja2')
        print(f'NNModel.cpp template path {NNModel_cpp_temp_file_path}')
        print(f'NNModel.cpp file path {NNModel_cpp_file_path}')

        try:
            NNModel_cpp_file = open(NNModel_cpp_file_path, "w")
        except OSError:
            print("Could not open NNModel.cpp file")
            return 'unable_generate'

        with NNModel_cpp_file:
            NNModel_cpp_codegen = NNModelCppCodegen()
            NNModel_cpp_codegen.code_gen(NNModel_cpp_file, NNModel_cpp_temp_file_path, self.model)

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
            main_codegen.code_gen(main_file, main_temp_file_path, self.vela_summary)
