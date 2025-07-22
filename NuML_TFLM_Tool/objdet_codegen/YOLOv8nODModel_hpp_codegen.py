import sys
import tflite
import os
from jinja2 import Environment, FileSystemLoader

def get_output_class(subgraph):
    #output tensors index
    output_tensor_indices = [subgraph.Outputs(i) for i in range(subgraph.OutputsLength())]
    for i, tensor_index in enumerate(output_tensor_indices):
        tensor = subgraph.Tensors(tensor_index)
        output_class = tensor.Shape(tensor.ShapeLength() - 1)
        if output_class != 64:
            return output_class
    return 0


def get_input_dimension(subgraph):
    tensor_index = subgraph.Inputs(0)
    tensor = subgraph.Tensors(tensor_index)
    input_dim = tensor.Shape(tensor.ShapeLength() - 2)
    return input_dim

def gen_max_operator_string(model):
    num_opcodes = model.OperatorCodesLength()
    szWriteLine = 'static constexpr int ms_maxOpCnt = ' + str(num_opcodes) + ';'
    return szWriteLine

class YOLOv8nODModelHppCodegen:
    def code_gen(self, NNModel_hpp_file, template_file, model_file):
        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        f = open(model_file, 'rb')
        buf = f.read()
        model = tflite.Model.GetRootAsModel(buf, 0)
        subgraph = model.Subgraphs(0)
        max_operators_str = gen_max_operator_string(model)
        input_dim = get_input_dimension(subgraph)
        output_class = get_output_class(subgraph)
        f.close()
        output = template.render(max_operators = max_operators_str, input_dim = input_dim, output_class = output_class)
        NNModel_hpp_file.write(output)
