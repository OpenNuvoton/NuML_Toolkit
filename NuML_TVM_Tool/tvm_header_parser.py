import sys
import re

def parser_input_tensor_name(tensor_name, header_file):
    while header_file:
        line = header_file.readline()
        if line == "":
            break
        nameObj = re.match(r'  void\* (\w*);', line)
        if nameObj == None:
            break
        tensor_name.append(nameObj.group(1))

def parser_out_tensor_name(tensor_name, header_file):
    while header_file:
        line = header_file.readline()
        if line == "":
            break
        nameObj = re.match(r'  void\* (\w*);', line)
        if nameObj == None:
            break
        tensor_name.append(nameObj.group(1))

def parser_device_name(device_name, header_file):
    while header_file:
        line = header_file.readline()
        if line == "":
            break
        nameObj = re.match(r'  void\* (\w*);', line)
        if nameObj == None:
            break
        device_name.append(nameObj.group(1))

input_tensor_list = ["tvmgen_default_inputs", parser_input_tensor_name, []]
output_tensor_list = ["tvmgen_default_outputs", parser_out_tensor_name, []]
device_name_list = ["tvmgen_default_devices", parser_device_name, []]

keyword_table = [input_tensor_list, output_tensor_list, device_name_list]

class HeaderParser:
    #Parse tvmgen_default.h
    def parser(self, header_file):
        while header_file:
            line = header_file.readline()
            if line == "":
                break
            for list_element in keyword_table:
                if re.search(list_element[0], line):
                    list_element[1](list_element[2], header_file)

    def get_input_tensor_name(self):
        return input_tensor_list[2]

    def get_output_tensor_name(self):
        return output_tensor_list[2]

    def get_device_name(self):
        return device_name_list[2]

