import sys
import re
from tvm_header_parser import HeaderParser

def gen_input_tensor_data_section(parser, main_file):
    input_tensor_name = parser.get_input_tensor_name()
    strDataSectionAttr = '__attribute__((aligned(16), section(".bss.noinit.tvm")))'
    for index in range(len(input_tensor_name)):
        szDataSzie = 'TVMGEN_DEFAULT_' + input_tensor_name[index].upper() + '_SIZE'
        szWriteLine = strDataSectionAttr + ' static uint8_t s_' + input_tensor_name[index] + '_buffer[' + szDataSzie + '];\n'
        main_file.write(szWriteLine)
    
def gen_onput_tensor_data_section(parser, main_file):
    output_tensor_name = parser.get_output_tensor_name()
    strDataSectionAttr = '__attribute__((aligned(16), section(".bss.noinit.tvm")))'
    for index in range(len(output_tensor_name)):
        szDataSzie = 'TVMGEN_DEFAULT_' + output_tensor_name[index].upper() + '_SIZE'
        szWriteLine = strDataSectionAttr + ' static uint8_t s_' + output_tensor_name[index] + '_buffer[' + szDataSzie + '];\n'
        main_file.write(szWriteLine)

def gen_ethous_irq_handler_section(parser, main_file):
    device_name = parser.get_device_name()
    if len(device_name) == 0:
        return
    for index in range(len(device_name)):
        if re.search("ethos_u", device_name[index]):
            main_file.write('#define ethosu_scratch          0\n')
            main_file.write('#define ETHOSU_FAST_MEMORY_SIZE 0\n')
            main_file.write('struct ethosu_driver ethosu0_driver;\n')
            main_file.write('void NPU_IRQHandler(void) {\n')
            main_file.write('\tethosu_irq_handler(&ethosu0_driver);\n')
            main_file.write('}\n')

def gen_ethous_init_section(parser, main_file):
    device_name = parser.get_device_name()
    if len(device_name) == 0:
        return
    for index in range(len(device_name)):
        if re.search("ethos_u", device_name[index]):
            main_file.write('#if defined(ARM_NPU)\n')
            main_file.write('\tstruct ethosu_driver *driver = ethosu_reserve_driver();\n')
            main_file.write('\tstruct tvmgen_default_devices devices = {\n')
            szWriteLine = '\t\t.' + device_name[index] + ' = driver,\n'
            main_file.write(szWriteLine)
            main_file.write('\t};\n')
            main_file.write('\tethosu_request_power(driver);\n')
            main_file.write('#endif\n')

def gen_input_tensor_init_section(parser, main_file):
    input_tensor_name = parser.get_input_tensor_name()
    main_file.write('\tstruct tvmgen_default_inputs inputs = {\n')
    for index in range(len(input_tensor_name)):
        szWriteLine = '\t\t.' + input_tensor_name[index] + ' = s_' + input_tensor_name[index] + '_buffer,\n'
        main_file.write(szWriteLine)
    main_file.write('\t};\n')

def gen_output_tensor_init_section(parser, main_file):
    output_tensor_name = parser.get_output_tensor_name()
    main_file.write('\tstruct tvmgen_default_outputs outputs = {\n')
    for index in range(len(output_tensor_name)):
        szWriteLine = '\t\t.' + output_tensor_name[index] + ' = s_' + output_tensor_name[index] + '_buffer,\n'
        main_file.write(szWriteLine)
    main_file.write('\t};\n')

def gen_ethosu_release_section(parser, main_file):
    device_name = parser.get_device_name()
    if len(device_name) == 0:
        return
    for index in range(len(device_name)):
        if re.search("ethos_u", device_name[index]):
            main_file.write('#if defined(ARM_NPU)\n')
            main_file.write('\tethosu_release_power(driver);\n')
            main_file.write('\tethosu_release_driver(driver);\n')
            main_file.write('#endif\n')  

def gen_ethosu_header_section(parser, main_file):
    device_name = parser.get_device_name()
    if len(device_name) == 0:
        return
    for index in range(len(device_name)):
        if re.search("ethos_u", device_name[index]):
            main_file.write('#if defined(ARM_NPU)\n')
            main_file.write('#include "ethosu_driver.h"\n')
            main_file.write('#endif\n')  


def gen_tvm_default_run_section(parser, main_file):
    device_name = parser.get_device_name()
    if len(device_name) == 0:
        main_file.write('\ttvmgen_default_run(&inputs, &outputs);\n')
    else:
        main_file.write('\ttvmgen_default_run(&inputs, &outputs, &devices);\n')

input_tensor_data_list = ["Input tensor data", gen_input_tensor_data_section]
output_tensor_data_list = ["Output tensor data", gen_onput_tensor_data_section]
ethsou_header_list = ["EthosU header", gen_ethosu_header_section]
ethsou_init_list = ["EthosU init", gen_ethous_init_section]
ethsou_release_list = ["EthosU release", gen_ethosu_release_section]
input_tensor_init_list = ["Input tensor init", gen_input_tensor_init_section]
output_tensor_init_list = ["Output tensor init", gen_output_tensor_init_section]
tvm_default_run_list = ["TVM default run", gen_tvm_default_run_section]

keyword_table = [input_tensor_data_list, output_tensor_data_list, ethsou_header_list, ethsou_init_list, ethsou_release_list, input_tensor_init_list, output_tensor_init_list, tvm_default_run_list]

class MainCCodegen:
    def code_gen(self, main_file, template_file, parser):
        while template_file:
            line = template_file.readline()
            if line == "":
                break
            main_file.write(line)
            if re.search("autogen section", line):
                for list_element in keyword_table:
                    if re.search(list_element[0], line):
                        line = template_file.readline()
                        main_file.write(line)
                        list_element[1](parser, main_file)

