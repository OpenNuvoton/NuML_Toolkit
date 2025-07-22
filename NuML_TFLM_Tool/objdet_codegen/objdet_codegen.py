import os

from objdet_codegen.YOLOv8nODModel_hpp_codegen import YOLOv8nODModelHppCodegen
from objdet_codegen.YOLOv8nODModel_cpp_codegen import YOLOv8nODModelCppCodegen
from objdet_codegen.Labels_cpp_codegen import LabelsCppCodegen
from objdet_codegen.YOLOv8nODPostProcessing_hpp_codegen import YOLOv8nODPostProcHppCodegen
from objdet_codegen.main_cpp_codegen import MainCCodegen

class ObjDetCodegen:
    def __init__(self, model, project, vela_summary, **kwargs):
        self.model = model
        self.project = project
        self.vela_summary = vela_summary
        self.extra = kwargs

    @classmethod
    def from_args(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    
    def code_gen(self):
        print('Run object detection codegen...')
        print(f"model:{self.model}")
        print(f"project:{self.project}")
        for key, value in self.extra.items():
            print(f"extra param:{key}, {value}")

        template_path = 'objdet_codegen'

        #Generate YOLOv8nODModel.hpp file
        NNModel_hpp_file_path = os.path.join(self.project, 'Model', 'include', 'YOLOv8nODModel.hpp')
        NNModel_hpp_temp_file_path = os.path.join(template_path, 'YOLOv8nODModel_hpp_tmpl.jinja2')
        print(f'YOLOv8nODModel.hpp template path {NNModel_hpp_temp_file_path}')
        print(f'YOLOv8nODModel.hpp file path {NNModel_hpp_file_path}')

        try:
            NNModel_hpp_file = open(NNModel_hpp_file_path, "w")
        except OSError:
            print("Could not open MobileNetModel.hpp file")
            return 'unable_generate'

        with NNModel_hpp_file:
            NNModel_hpp_codegen = YOLOv8nODModelHppCodegen()
            NNModel_hpp_codegen.code_gen(NNModel_hpp_file, NNModel_hpp_temp_file_path, self.model)

        #Generate YOLOv8nODModel.cpp file
        NNModel_cpp_file_path = os.path.join(self.project, 'Model', 'YOLOv8nODModel.cpp')
        NNModel_cpp_temp_file_path = os.path.join(template_path, 'YOLOv8nODModel_cpp_tmpl.jinja2')
        print(f'YOLOv8nODModel.cpp template path {NNModel_cpp_temp_file_path}')
        print(f'YOLOv8nODModel.cpp file path {NNModel_cpp_file_path}')

        try:
            NNModel_cpp_file = open(NNModel_cpp_file_path, "w")
        except OSError:
            print("Could not open MobileNetModel.cpp file")
            return 'unable_generate'

        with NNModel_cpp_file:
            NNModel_cpp_codegen = YOLOv8nODModelCppCodegen()
            NNModel_cpp_codegen.code_gen(NNModel_cpp_file, NNModel_cpp_temp_file_path, self.model)

        #Generate Labels.cpp file
        Labels_cpp_file_path = os.path.join(self.project, 'Model', 'Labels.cpp')
        Labels_cpp_temp_file_path = os.path.join(template_path, 'Labels_cpp_tmpl.jinja2')
        print(f'Labels.cpp template path {Labels_cpp_temp_file_path}')
        print(f'Labels.cpp file path {Labels_cpp_file_path}')

        try:
            Lables_cpp_file = open(Labels_cpp_file_path, "w")
        except OSError:
            print("Could not open Labels.cpp file")
            return 'unable_generate'

        with Lables_cpp_file:
            Labels_codegen = LabelsCppCodegen()
            Labels_codegen.code_gen(Lables_cpp_file, Labels_cpp_temp_file_path, self.model)

        #Generate YOLOv8nODPostProcessing.hpp file
        PostProc_hpp_file_path = os.path.join(self.project, 'YOLOv8nODPostProcessing.hpp')
        PostProc_hpp_temp_file_path = os.path.join(template_path, 'YOLOv8nODPostProcessing_hpp_tmpl.jinja2')
        print(f'YOLOv8nODPostProcessing.hpp template path {PostProc_hpp_temp_file_path}')
        print(f'YOLOv8nODPostProcessing.hpp file path {PostProc_hpp_file_path}')

        try:
            PostProc_hpp_file = open(PostProc_hpp_file_path, "w")
        except OSError:
            print("Could not open Labels.cpp file")
            return 'unable_generate'

        with PostProc_hpp_file:
            PostProc_codegen = YOLOv8nODPostProcHppCodegen()
            PostProc_codegen.code_gen(PostProc_hpp_file, PostProc_hpp_temp_file_path, self.model)

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
