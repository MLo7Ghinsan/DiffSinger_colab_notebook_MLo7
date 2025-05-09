## TODO

- [x] Support multidict training on main notebook.
- [ ] OpenUtau export for multidict compatibility
- [x] Inference cell inside training/Inference notebook.
- [ ] Improve SOFA notebook.

___

### Custom Local Training GUI is moved to [DiffTrainer](https://github.com/agentasteriski/DiffTrainer)

___

### Want to render on CLI for a quick test? Use the [Inference notebook. ](Diffsinger_Inference_CLI.ipynb)More info on [inference.md](inference.md)
___

### Please see [data_example.md](https://github.com/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/blob/main/data_example.md) for the data setup format
___

## DiffSinger training notebook: <a href="https://colab.research.google.com/github/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/blob/main/DiffSinger_colab_notebook.ipynb"> <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 150px;"/> </a>

### current supported data format:
- lab + wav (NNSVS format)
- csv + wav (DiffSinger format)
- ds (DiffSinger .ds files)

#### NOTE:

- your_speaker_folder's folder name will be used as *spk_name* so please be careful about your file naming
- colab notebook primarily uses python; thus space and special character in file name or folder path may be invalid
- for an in-depth guide for SVS training and/or labeling, please see [SVS Singing Voice Database - Tutorial](https://docs.google.com/document/d/1uMsepxbdUW65PfIWL1pt2OM6ZKa5ybTTJOpZ733Ht6s/edit?usp=sharing)
- it is advised to edit your data using [SlurCutter](https://github.com/openvpi/MakeDiffSinger/releases) for a more refined data for your pitch model
- please visit [DiffSinger Discord](https://discord.com/invite/wwbu2JUMjj) for any help and questions regarding model production

Zip file format [examples](https://github.com/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/releases/tag/ref):
___

## Vocoder finetuning notebook: <a href="https://github.com/usamireko/DiffSinger_colab_notebook_MLo7/blob/main/PC_NSF_NSF_hifigan_finetuning_notebook.ipynb"> <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 150px;"/> </a>

### current supported data format:
- wav

#### NOTE:

- it is suggested to use manual segmented audio for cleaner segments (though there's minimal difference when using the auto segmentation)
- zip file format can consist of any type of files, even subfolders. data extraction will only account .wav that are within the zip into the training set
___

## SOFA training notebook (wip): <a href="https://github.com/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/blob/main/SOFA_Notebook.ipynb"> <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 150px;"/> </a>

### current supported data format:
- lab + wav (NNSVS format)

#### NOTE:

- this notebook is still a rough draft, please either don't use it at all or use it with caution....

___

#### Plans (update might not be in order):

- [notebook] improve SOFA notebook, add inference
- [notebook] update dictionary conversion code for phoneme types in build OU
- [notebook] clean up multi-dict notebook and support logic for dictionary generating for out-of-spefied-lang labels (/)
- [resource] add example file(s) for multi-dicitonary training

___

**Credits:** 

  - [openvpi](https://openvpi.github.io/) for DiffSinger fork and more

  - [UtaUtaUtau](https://utautautau.neocities.org/) for nnsvs-db-converter

  - [Kei](https://pronouns.page/@kei.wendt06) for the original notebook

  - [MLo7](https://github.com/MLo7Ghinsan) for the repo's content

  - [PixPrucer](https://twitter.com/PixPrucer?s=20) for an in-depth SVS guide
    
  - [haru0l](https://x.com/mscoocoo2?s=20) for the base pretrain with embeds

  - [AgentAsteriski](https://github.com/agentasteriski) for the local GUI
    
