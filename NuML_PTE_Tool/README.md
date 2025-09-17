NuML_Tool
===
### Machine learning MCU project generate, build and flash utility. Base on ExecuTorch framework. 
## Support list
* Board 
    1. NuMaker-M55M1
* Project type (IDE/toolchain)
    1. uvision5/armc6
    2. make/gcc
## Install
~~~
pip install -r ..\requirements.txt  
python setup_progendef.py
~~~  
* Arm GNU toolcahin
    1. Download from https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads
    2. Install and add installation direcoty to your windows user Path environment variable
## Usage
* Generate
    ~~~
    python numl_tool.py generate --pte_file ..\models\mv2.pte --board NuMaker-M55M1 --output_path ..\NuML_Gen [--project_type uvision5_armc6]
    ~~~  
    * Parameter  
        * pte_file: A ExecuTorch PTE file which supported Arm EthosU backend. You should follow [Arm(R) Ethos(TM)-U NPU Backend](https://docs.pytorch.org/executorch/stable/backends-arm-ethos-u.html) tutorial to convert the PTE file. The "models\mv2.pte" file is only for testing.
        * board: Supported board name  
            * NuMaker_M55M1
        * output_path: Ouput directory path of generated project
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
        * application [option]: Specify application scenario
            * generic - default
* Build
    ~~~
    python numl_tool.py build --project_path ..\NuML_Gen\ProjGen_NuMaker_M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference [--project_type uvision5_armc6] [--ide_tool C:\Keil_v5\UV4\UV4.exe]
    ~~~
    * Parameter
        * project_path: Generated project directory
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
        * ide_tool [uVision5 option]: UV4.exe path 
* Flash
    ~~~
    python numl_tool.py flash --project_path ..\NuML_Gen\ProjGen_NuMaker_M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference --board NuMaker-M55M1 [--project_type uvision5_armc6]
    ~~~
    * Parameter
        * project_path: Generated project directory
        * board: Supported board name
            * NuMaker_M55M1
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
* Deploy
    ~~~
    python numl_tool.py deploy --pte_file ..\models\mv2.pte --board NuMaker-M55M1 --output_path ..\NuML_Gen [--project_type uvision5_armc6] [--ide_tool C:\Keil_v5\UV4\UV4.exe]
    ~~~
    * Parameter
        * pte_file: A ExecuTorch PTE file which supported Arm EthosU backend. You should follow [Arm(R) Ethos(TM)-U NPU Backend](https://docs.pytorch.org/executorch/stable/backends-arm-ethos-u.html) tutorial to convert the PTE file. The "models\mv2.pte" file is only for testing.
        * board: Supported board name  
            * NuMaker_M55M1
        * output_path: Ouput directory path of generated project
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
        * ide_tool [uVision5 option]: UV4.exe path 
## Example
* For make_gcc_arm
    ~~~
    python numl_tool generate --pte_file ..\models\mv2.pte --board NuMaker-M55M1 --output_path ..\NuML_Gen
    python numl_tool.py build --project_path ..\NuML_Gen\ProjGen_NuMaker_M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference   
    python numl_tool.py flash --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference --board NuMaker-M55M1    
    ~~~
    or
    ~~~
    python numl_tool.py deploy --pte_file ..\models\mv2.pte --board NuMaker-M55M1 --output_path ..\NuML_Gen    
    ~~~
* For uvision5_armc6
    ~~~
    python numl_tool.py generate --pte_file ..\models\mv2.pte --board NuMaker-M55M1 --output_path ..\NuML_Gen --project_type uvision5_armc6
    python numl_tool.py build --project_path ..\NuML_Gen\ProjGen_NuMaker_M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference --project_type uvision5_armc6 --ide_tool C:\Keil_v5\UV4\UV4.exe   
    python numl_tool.py flash --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference --board NuMaker-M55M1 --project_type uvision5_armc6
    ~~~
    or
    ~~~
    python numl_tool.py deploy --pte_file ..\models\mv2.pte --board NuMaker-M55M1 --output_path ..\NuML_Gen --project_type uvision5_armc6 --ide_tool C:\Keil_v5\UV4\UV4.exe
    ~~~
