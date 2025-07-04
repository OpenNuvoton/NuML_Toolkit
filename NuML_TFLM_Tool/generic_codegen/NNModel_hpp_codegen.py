import sys
import tflite
import os
from jinja2 import Environment, FileSystemLoader

def gen_max_operator_string(model_file):
    f = open(model_file, 'rb')
    buf = f.read()
    model = tflite.Model.GetRootAsModel(buf, 0)
    subgraph = model.Subgraphs(0)
    num_opcodes = model.OperatorCodesLength()
    f.close()
    szWriteLine = 'static constexpr int ms_maxOpCnt = ' + str(num_opcodes) + ';'
    return szWriteLine

class NNModelHppCodegen:
    def code_gen(self, NNModel_hpp_file, template_file, model_file):
        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        max_operators_str = gen_max_operator_string(model_file)
        output = template.render(max_operators = max_operators_str)
        NNModel_hpp_file.write(output)

