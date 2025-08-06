NuML_Toolkit
===
### Windows tools for Nuvoton machine learning platform.
## Tools 
* [NuML_TFLM_Tool](NuML_TFLM_Tool\README.md) : Tool for machine learning project generate, build and flash base on TFLM framework
* [NuML_TVM_Tool](NuML_TVM_Tool\README.md): Tool for machine learning project generate, build and flash base on TVM framwwork
* [NuML_Dashboard](NuML_Dashboard\README.md): Web GUI for NuML_Tool_TFLM 
* tvmc: TVM model compiler  
    Reference: https://tvm.apache.org/docs/tutorial/tvmc_command_line_driver.html
* vela: Arm model compiler for NPU accelerator  
    Reference: https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-vela
* tools: make and NuLink command tool
* tflite2cpp: tflite model file convert to CPP hearder file
## Install  
1. Python 3.8 environment  
    For conda:  
    ~~~
    conda env create --file conda\environment.yml
    ~~~  
    For others:  
    ~~~
    pip install -r requirements.txt
    ~~~  
2. tvmc.exe download  
    ~~~
    cd tvmc
    python tvmc_exe_download.py
    ~~~

