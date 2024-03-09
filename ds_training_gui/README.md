### python 3.10 was used and is recommended

required modules:
- PyYAML
- tk
- tqdm
- requests

a dedicated conda environment is suggested, but not required
___

### how to use:

1. run setup_gui.bat ***The GUI will not launch without its dependencies***
2. run run_gui.bat

setup_gui.bat only needed to be executed once since it's only for installing dependencies
so just run run_gui.bat if you already have all the dependencies
___

### notes:
- If running the script by itself and nothing happens, please run the gui script through command line

- If training doesn't detect user's GPU, please make sure that you have installed torch with cuda
___

### known issues & quirks:
- download dependencies does not detect cuda for torch version, cuda users please ~~reinstall torch with cuda from command line~~ use the (yes CUDA) download option
  
- after editing configs or preprocessing, the gui develops amnesia and forgets where it is. relaunch
___

### intended future additions:
- onnx exports and set up for use in openutau
  
- ~~button to update only diffsinger and db converter files~~
