import sys
import os
import shutil

#get site packages pth
site_packages = next(p for p in sys.path if 'site-packages' in p)
print(site_packages)

sys_progendef_path = os.path.join(site_packages, 'project_generator_definitions')
nvt_progendef_path = os.path.join(os.path.dirname(__file__), 'progen_mcu_definitions')

if not os.path.exists(sys_progendef_path):
    print('Unable find project_generator_definitions path')
    exit(-1)

#copy Nuvoton MCU default definitation to site_packages/project_generator_definitions\mcu
shutil.copytree(os.path.join(nvt_progendef_path, 'mcu', 'nuvoton'), os.path.join(sys_progendef_path, 'mcu', 'nuvoton'), dirs_exist_ok = True)

#update site_packages/project_generator_definitions\target\target.py
shutil.copyfile(os.path.join(nvt_progendef_path, 'target', 'targets.py'), os.path.join(sys_progendef_path, 'target', 'targets.py'))
