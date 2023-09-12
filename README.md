# DiffSinger_colab_notebook_MLo7
### MLo7 DiffSinger training colab notebook an edited copy of Kei's DiffSinger colab notebook

### current supported data format:
- lab + wav (NNSVS format)
- csv + wav (DiffSinger format)
- ds + wav (DiffSinger format)

(textgrid/OpenCpop format is not supported at the moment)

## Access the notebook here: <a href="https://colab.research.google.com/github/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/blob/main/DiffSinger_colab_notebook.ipynb"> <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 150px;"/> </a>
___
### Below is from the notebook's expansion
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

**Credits:** 

  - [openvpi](https://openvpi.github.io/) for DiffSinger fork and more

  - [UtaUtaUtau](https://utautautau.neocities.org/) for nnsvs-db-converter

  - [Kei](https://pronouns.page/@kei.wendt06) for the original notebook

  - [MLo7](https://github.com/MLo7Ghinsan) for the notebook edit

  - [PixPrucer](https://twitter.com/PixPrucer?s=20) for an in-depth SVS guide
