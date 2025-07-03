import sys
import pandas
import os
from jinja2 import Environment, FileSystemLoader

FLASH_SIZE_LIMIT = 1.4 * 1024000

def add_activation_size_section(sram_usage, flash_usage):
    activation_size = int(sram_usage * 1.4)
    activation_size &= ~(1024 - 1)
    szWriteLine = '#define ACTIVATION_BUF_SZ (' + str(activation_size) + ')'
    return szWriteLine

def add_model_load_section(sram_usage, flash_usage):
    if flash_usage > FLASH_SIZE_LIMIT:
        szWriteLine = '#define __LOAD_MODEL_FROM_SD__'
    else :
        szWriteLine = '//#define __LOAD_MODEL_FROM_SD__'
    return szWriteLine

#parse vela summary file to get memory usage information
def vela_summary_parse(summary_file):
    usecols = ['sram_memory_used', 'off_chip_flash_memory_used']
    df = pandas.read_csv(summary_file, usecols=usecols)
    return df.iloc[0,0]*1024, df.iloc[0,1]*1024 

class MainCCodegen:
    def code_gen(self, main_file, template_file, vela_summary_file):

        #get model memory usage information from vela summary output file
        model_sram_usage, model_flash_usage = vela_summary_parse(vela_summary_file)
        print(model_sram_usage)
        print(model_flash_usage)

        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        model_load_str = add_model_load_section(model_sram_usage, model_flash_usage)
        activation_buf_str = add_activation_size_section(model_sram_usage, model_flash_usage)
        output = template.render(define_SD_model_load = model_load_str, define_activation_buf_size = activation_buf_str)
        main_file.write(output)
