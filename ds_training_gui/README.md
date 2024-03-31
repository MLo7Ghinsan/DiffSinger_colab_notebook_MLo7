### python 3.10 was used and is recommended

required modules:
- PyYAML
- tk
- tqdm
- requests

a dedicated conda environment is suggested, but not required
___

### how to use:

simply just run run_gui.bat after you installed or have pYthon 3.10
___

### notes:
- If running the script by itself and nothing happens, please run the gui script through command line

- If training doesn't detect user's GPU, please make sure that you have installed torch with cuda
___

### known issues & quirks:
- export onnx will create a backup of the previous version, but fails if there's already a backup copy
  
- training individual parameters is not currently compatible with OU VB builder
___

### intended future additions:
- ~~onnx exports and set up for use in openutau~~
  
- ~~button to update only diffsinger and db converter files~~

- full redesign in customtkinter

- default dsdicts
