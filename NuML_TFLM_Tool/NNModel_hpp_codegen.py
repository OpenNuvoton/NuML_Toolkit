import sys
import re
import tflite

def gen_max_operator_section(model_file, NNModel_hpp_file):
    buf = open(model_file, 'rb').read()
    model = tflite.Model.GetRootAsModel(buf, 0)
    subgraph = model.Subgraphs(0)
    num_opcodes = model.OperatorCodesLength()
    szWriteLine = '\tstatic constexpr int ms_maxOpCnt = ' + str(num_opcodes) + ';\n'
    NNModel_hpp_file.write(szWriteLine)

max_operator_list = ["Max Operator Count", gen_max_operator_section]
keyword_table = [max_operator_list]

class NNModelHppCodegen:
    def code_gen(self, NNModel_hpp_file, template_file, model_file):
        while template_file:
            line = template_file.readline()
            if line == "":
                break
            NNModel_hpp_file.write(line)
            if re.search("autogen section", line):
                for list_element in keyword_table:
                    if re.search(list_element[0], line):
                        line = template_file.readline()
                        NNModel_hpp_file.write(line)
                        list_element[1](model_file, NNModel_hpp_file)
