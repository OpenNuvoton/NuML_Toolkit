NuML_Tool
===
### Machine learning MCU project generate, build and flash utility. Base on TVM framework. 
## Support list
* Board 
    1. NuMaker-M55M1
    2. NuMaker-M467
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
    python numl_tool.py generate --model_file ..\models\vww4_128_128_INT8.tflite --board NuMaker-M55M1 --output_path ..\NuML_Gen [--project_type uvision5_armc6]
    ~~~  
    * Parameter  
        * model_file: A quantized tflite model. You can refer to the [NuEdgeWise](https://github.com/OpenNuvoton/NuEdgeWise) tutorial to train your model. The "models\vww4_128_128_INT8.tflite" file is only for testing.
        * board: Supported board name  
            * NuMaker-M55M1
            * NuMaker-M467
        * output_path: Ouput directory path of generated project
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
* Build
    ~~~
    python numl_tool.py build --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1 [--ide_tool C:\Keil_v5\UV4\UV4.exe]
    ~~~
    * Parameter
        * project_path: Generated project directory
        * ide_tool [uVision5 option]: UV4.exe path 
* Flash
    ~~~
    python numl_tool.py flash --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1 --board NuMaker-M55M1 [--project_type uvision5_armc6]
    ~~~
    * Parameter
        * project_path: Generated project directory
        * board: Supported board name
            * NuMaker-M55M1
            * NuMaker-M467
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
* deploy
    ~~~
    python numl_tool.py deploy --model_file ..\models\vww4_128_128_INT8.tflite --board NuMaker-M55M1 --output_path ..\NuML_Gen [--project_type uvision5_armc6] [--ide_tool C:\Keil_v5\UV4\UV4.exe]
    ~~~
    * Parameter
        * model_file: A quantized tflite model. You can refer to the [NuEdgeWise](https://github.com/OpenNuvoton/NuEdgeWise) tutorial to train your model. The "models\vww4_128_128_INT8.tflite" is only for testing.
        * board: Supported board name  
            * NuMaker-M55M1
            * NuMaker-M467
        * output_path: Ouput directory path of generated project
        * project_type [option]: Specify generated project type  
            * make_gcc_arm - default
            * uvision5_armc6  
        * ide_tool [uVision5 option]: UV4.exe path 
## Example
* For make_gcc_arm
    ~~~
    python numl_tool generate --model_file ..\models\vww4_128_128_INT8.tflite --board NuMaker-M55M1 --output_path ..\NuML_Gen
    python numl_tool.py build --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1   
    python numl_tool.py flash --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1 --board NuMaker-M55M1    
    ~~~
    or
    ~~~
    python numl_tool.py deploy --model_file ..\models\vww4_128_128_INT8.tflite --board NuMaker-M55M1 --output_path ..\NuML_Gen    
    ~~~
* For uvision5_armc6
    ~~~
    python numl_tool.py generate --model_file ..\models\vww4_128_128_INT8.tflite --board NuMaker-M55M1 --output_path ..\NuML_Gen --project_type uvision5_armc6
    python numl_tool.py build --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1 --ide_tool C:\Keil_v5\UV4\UV4.exe   
    python numl_tool.py flash --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1 --board NuMaker-M55M1 --project_type uvision5_armc6
    ~~~
    or
    ~~~
    python numl_tool.py deploy --model_file ..\models\vww4_128_128_INT8.tflite --board NuMaker-M55M1 --output_path ..\NuML_Gen --project_type uvision5_armc6 --ide_tool C:\Keil_v5\UV4\UV4.exe
    ~~~
