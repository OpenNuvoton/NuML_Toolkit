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

class LabelsCppCodegen:
    def code_gen(self, Labels_cpp_file, template_file, model_file):
        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        f = open(model_file, 'rb')
        buf = f.read()
        model = tflite.Model.GetRootAsModel(buf, 0)
        subgraph = model.Subgraphs(0)
        lables_size = get_output_class(subgraph)
        labels = [ i for i in range(lables_size) ]
        f.close()
        output = template.render(labels = labels, labels_size = lables_size)
        Labels_cpp_file.write(output)
