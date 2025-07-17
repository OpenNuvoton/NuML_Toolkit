NuML_Tool
===
### Machine learning MCU project generate, build and flash utility. Base on TFLM framework. 
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
    python numl_tool.py generate --model_file xxx\xxx.tflte --board NuMaker-M55M1 --output_path ..\..\yyy [--project_type uvision5_armc6]
    ~~~  
    * Parameter  
        * model_file: Specify neraual network model file
        * board: Supported board name  
            * NuMaker_M55M1
        * output_path: Ouput directory path of generated project
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
        * application [option]: Specify application scenario
            * generic - default
            * imgclass  
        * model_arena_size [option]: Specify the size of arena cache memory in bytes
* Build
    ~~~
    python numl_tool.py build --project_path ..\..\yyy\ProjGen_NuMaker_M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference [--project_type uvision5_armc6] [--ide_tool C:\Keil_v5\UV4\UV4.exe]
    ~~~
    * Parameter
        * project_path: Generated project directory
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
        * ide_tool [uVision5 option]: UV4.exe path 
* Flash
    ~~~
    python numl_tool.py flash --project_path ..\..\yyy\ProjGen_NuMaker_M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference --board NuMaker-M55M1 [--project_type uvision5_armc6]
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
    python numl_tool.py deploy --model_file xxx\xxx.tflte --board NuMaker-M55M1 --output_path ..\..\yyy [--project_type uvision5_armc6] [--ide_tool C:\Keil_v5\UV4\UV4.exe]
    ~~~
    * Parameter
        * model_file: Specify neraual network model file
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
    python numl_tool generate --model_file xxx\xxx.tflte --board NuMaker-M55M1 --output_path ..\..\yyy
    python numl_tool.py build --project_path ..\..\yyy\ProjGen_NuMaker_M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference   
    python numl_tool.py flash --project_path ..\..\yyy\ProjGen_NuMaker-M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference --board NuMaker-M55M1    
    ~~~
    or
    ~~~
    python numl_tool.py deploy --model_file xxx\xxx.tflte --board NuMaker-M55M1 --output_path ..\..\yyy    
    ~~~
* For uvision5_armc6
    ~~~
    python numl_tool.py generate --model_file xxx\xxx.tflte --board NuMaker-M55M1 --output_path ..\..\yyy --project_type uvision5_armc6
    python numl_tool.py build --project_path ..\..\yyy\ProjGen_NuMaker_M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference --project_type uvision5_armc6 --ide_tool C:\Keil_v5\UV4\UV4.exe   
    python numl_tool.py flash --project_path ..\..\yyy\ProjGen_NuMaker-M55M1\M55M1BSP\SampleCode\MachineLearning\NN_ModelInference --board NuMaker-M55M1 --project_type uvision5_armc6
    ~~~
    or
    ~~~
    python numl_tool.py deploy --model_file xxx\xxx.tflte --board NuMaker-M55M1 --output_path ..\..\yyy --project_type uvision5_armc6 --ide_tool C:\Keil_v5\UV4\UV4.exe
    ~~~
