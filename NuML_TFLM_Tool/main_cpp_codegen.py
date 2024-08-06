import sys
import re
import pandas

FLASH_SIZE_LIMIT = 1.4 * 1024000

def add_activation_size_section(main_cpp_file, sram_usage, flash_usage):
    activation_size = int(sram_usage * 1.4)
    activation_size &= ~(1024 - 1)
    szWriteLine = '#define ACTIVATION_BUF_SZ (' + str(activation_size) + ')\n'

    main_cpp_file.write(szWriteLine)

def add_model_load_section(main_cpp_file, sram_usage, flash_usage):
    if flash_usage > FLASH_SIZE_LIMIT:
        szWriteLine = '#define __LOAD_MODEL_FROM_SD__\n'
    else :
        szWriteLine = '//#define __LOAD_MODEL_FROM_SD__\n'

    main_cpp_file.write(szWriteLine)

#parse vela summary file to get memory usage information
def vela_summary_parse(summary_file):
    usecols = ['sram_memory_used', 'off_chip_flash_memory_used']
    df = pandas.read_csv(summary_file, usecols=usecols)
    return df.iloc[0,0]*1024, df.iloc[0,1]*1024 


model_sd_list = ["Model in SD", add_model_load_section]
activation_size_list = ["Activation size", add_activation_size_section]

keyword_table = [model_sd_list, activation_size_list]

class MainCCodegen:
    def code_gen(self, main_file, template_file, vela_summary_file):

        #get model memory usage information from vela summary output file
        model_sram_usage, model_flash_usage = vela_summary_parse(vela_summary_file)
        print(model_sram_usage)
        print(model_flash_usage)

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
                        list_element[1](main_file, model_sram_usage, model_flash_usage)