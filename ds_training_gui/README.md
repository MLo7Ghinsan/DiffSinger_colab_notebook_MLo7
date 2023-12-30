### python 3.10 was used and is recommended

required modules:
- PyYAML
- tk
- tqdm
- requests
a dedicated conda environment is suggested, but not required

run `pip install PyYAML tk tqdm requests` if you don't have these modules


### notes:
- If running the script by itself and nothing happens, please run the gui script through commandline

- If training doesn't detect user's GPU, please make sure that you have installed torch with cuda

### known issues & quirks:
- download dependencies does not detect cuda for torch version, cuda users please reinstall torch with cuda from command line
- after editing configs or preprocessing, the gui develops amnesia and forgets where it is. relaunch

### intended future additions:
- onnx exports and set up for use in openutau
- button to update only diffsinger and db converter files
