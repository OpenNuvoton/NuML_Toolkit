import sys
import tflite
import os
from jinja2 import Environment, FileSystemLoader

def get_input_dimension(subgraph):
    tensor_index = subgraph.Inputs(0)
    tensor = subgraph.Tensors(tensor_index)
    input_dim = tensor.Shape(tensor.ShapeLength() - 2)
    return input_dim

def get_output_tensor_index(subgraph, input_dim):
    #output tensors index
    stride8_dim = input_dim / 8
    stride8_dim = stride8_dim * stride8_dim

    stride16_dim = input_dim / 16
    stride16_dim = stride16_dim * stride16_dim

    stride32_dim = input_dim / 32
    stride32_dim = stride32_dim * stride32_dim

    output_tensor_indices = [subgraph.Outputs(i) for i in range(subgraph.OutputsLength())]

    for i, tensor_index in enumerate(output_tensor_indices):
        tensor = subgraph.Tensors(tensor_index)
        shape_len = tensor.ShapeLength()
        stride_dim = tensor.Shape(shape_len - 2) 
        box_conf = tensor.Shape(shape_len - 1)

        if stride_dim == stride8_dim:
            if box_conf == 64:
                stride8_box_index = i
            else:
                stride8_conf_index = i

        if stride_dim == stride16_dim:
            if box_conf == 64:
                stride16_box_index = i
            else:
                stride16_conf_index = i

        if stride_dim == stride32_dim:
            if box_conf == 64:
                stride32_box_index = i
            else:
                stride32_conf_index = i
    return stride8_conf_index, stride16_conf_index , stride32_conf_index, stride8_box_index, stride16_box_index, stride32_box_index

class YOLOv8nODPostProcHppCodegen:
    def code_gen(self, post_proc_hpp_file, template_file, model_file):
        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        f = open(model_file, 'rb')
        buf = f.read()
        model = tflite.Model.GetRootAsModel(buf, 0)
        subgraph = model.Subgraphs(0)
        input_dim = get_input_dimension(subgraph)
        stride8_conf, stride16_conf, stride32_conf, stride8_box, stride16_box, stride32_box = get_output_tensor_index(subgraph, input_dim)
        f.close()
        output = template.render(stride8_conf_index = stride8_conf, stride16_conf_index = stride16_conf, stride32_conf_index = stride32_conf, stride8_box_index = stride8_box, stride16_box_index = stride16_box, stride32_box_index = stride32_box)
        post_proc_hpp_file.write(output)
