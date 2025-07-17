import sys
import tflite
import os
from jinja2 import Environment, FileSystemLoader

def add_lables_section(model_file):
    f = open(model_file, 'rb')
    buf = f.read()
    model = tflite.Model.GetRootAsModel(buf, 0)
    subgraph = model.Subgraphs(0)
    tensor_index = subgraph.Outputs(0)
    tensor = subgraph.Tensors(tensor_index)
    lables_size = tensor.Shape(tensor.ShapeLength() - 1)
    labels = [ i for i in range(lables_size) ]
    f.close()
    return labels, lables_size

class LabelsCppCodegen:
    def code_gen(self, Labels_cpp_file, template_file, model_file):
        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        labels, lables_size = add_lables_section(model_file)
        output = template.render(labels = labels, labels_size = lables_size)
        Labels_cpp_file.write(output)
