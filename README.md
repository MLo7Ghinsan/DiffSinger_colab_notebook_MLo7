# DiffSinger_colab_notebook_MLo7
### MLo7 DiffSinger training colab notebook an edited copy of Kei's DiffSinger colab notebook

### current supported data format:
- lab + wav (NNSVS format)
- csv + wav (DiffSinger format)
- ~~ds + wav (DiffSinger format)~~ broken

## Access the notebook here: <a href="https://colab.research.google.com/github/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/blob/main/DiffSinger_colab_notebook.ipynb"> <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 150px;"/> </a>
___

#### GUI note:
python 3.10 was used and is recommended

please run ```pip install PyYAML tk tqdm requests``` if you don't have these modules (the are necessary for the gui)

___

#### IMPORTANT NOTE:

- your_speaker_folder's folder name will be used as *spk_name* so please be careful about your file naming
- colab notebook primarily uses python; thus space in file name or folder path may be invalid
- for an in-depth guide for SVS training and/or labeling, please see [SVS Singing Voice Database - Tutorial](https://docs.google.com/document/d/1uMsepxbdUW65PfIWL1pt2OM6ZKa5ybTTJOpZ733Ht6s/edit?usp=sharing)

This notebook converts your data (lab + wav) to compatible format via [nnsvs-db-converter](https://github.com/UtaUtaUtau/nnsvs-db-converter)

It is advised to edit your data using [SlurCutter](https://github.com/openvpi/MakeDiffSinger/releases) for a more refined data for your pitch model

Zip file format [example](https://github.com/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/releases/tag/ref):
<pre>
#single speaker (lab + wav | ds + wav)
your_zip.zip:
    |
    |
    your_speaker_folder:
        |
        |
        data_1.wav
        data_1.lab (or.ds)
        .
        data_2.wav
        data_2.lab (or.ds)
        .
        data_3.wav
        data_3.lab (or.ds)
        .
        ...
</pre>
<pre>
#single speaker (csv + wav)
your_zip.zip:
    |
    |
    your_speaker_folder:
        |
        |
        wavs (folder named "wavs" containing all the wavs)
        .
        transcriptions.csv
</pre>
<pre>
#multi speaker (lab + wav | ds + wav)
your_zip.zip:
    |
    |
    your_speaker_folder_1:
        |
        |
        data_1.wav
        data_1.lab (or.ds)
        .
        data_2.wav
        data_2.lab (or.ds)
        .
        data_3.wav
        data_3.lab (or.ds)
        .
        ...
    your_speaker_folder_2:
        |
        |
        data_1.wav
        data_1.lab (or.ds)
        .
        data_2.wav
        data_2.lab (or.ds)
        .
        data_3.wav
        data_3.lab (or.ds)
        .
        ...
</pre>
<pre>
#multi speaker (csv + wav)
your_zip.zip:
    |
    |
    your_speaker_folder_1:
        |
        |
        wavs (folder named "wavs" containing all the wavs)
        .
        transcriptions.csv
    your_speaker_folder_2:
        |
        |
        wavs (folder named "wavs" containing all the wavs)
        .
        transcriptions.csv

</pre>

___

#### Plans (update might not be in order):

- [script] add onnx exporter to ds_gui.py
- [jupyter] overhaul ou build section
- [jupyter] add option to use pretrained model
- [jupyter] make NSF-HiFiGAN vocoder training notebook via [fish-diffusion](https://github.com/fishaudio/fish-diffusion)

___

**Credits:** 

  - [openvpi](https://openvpi.github.io/) for DiffSinger fork and more

  - [UtaUtaUtau](https://utautautau.neocities.org/) for nnsvs-db-converter

  - [Kei](https://pronouns.page/@kei.wendt06) for the original notebook

  - [MLo7](https://github.com/MLo7Ghinsan) for the notebook edit

  - [PixPrucer](https://twitter.com/PixPrucer?s=20) for an in-depth SVS guide

___

#### Extra Note:

Wow you made it to the very bottom.... Why though lmao hahahahhshahhasdksajidhasjl

Feel free to suggest or ask any question via [discord](https://discord.com/invite/wwbu2JUMjj) my user display name is MLo7 and my user name is ghin_mlo7
