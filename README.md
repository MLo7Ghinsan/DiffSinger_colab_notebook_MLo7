### current supported data format:
- lab + wav (NNSVS format)
- csv + wav (DiffSinger format)
- ds + wav (DiffSinger format)

## Access the notebook here: <a href="https://colab.research.google.com/github/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/blob/main/DiffSinger_colab_notebook.ipynb"> <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 150px;"/> </a>
___

#### IMPORTANT NOTE:

- your_speaker_folder's folder name will be used as *spk_name* so please be careful about your file naming
- colab notebook primarily uses python; thus space in file name or folder path may be invalid
- for an in-depth guide for SVS training and/or labeling, please see [SVS Singing Voice Database - Tutorial](https://docs.google.com/document/d/1uMsepxbdUW65PfIWL1pt2OM6ZKa5ybTTJOpZ733Ht6s/edit?usp=sharing)
- it is advised to edit your data using [SlurCutter](https://github.com/openvpi/MakeDiffSinger/releases) for a more refined data for your pitch model
- please visit [DiffSinger Discord](https://discord.com/invite/wwbu2JUMjj) for any help and questions regarding model production

Zip file format [examples](https://github.com/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/releases/tag/ref):
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

- [doc] add an easy "how to create a DiffSinger model" document
- [doc] add video(s) of model making process (quick notebook guide)

___

**Credits:** 

  - [openvpi](https://openvpi.github.io/) for DiffSinger fork and more

  - [UtaUtaUtau](https://utautautau.neocities.org/) for nnsvs-db-converter

  - [Kei](https://pronouns.page/@kei.wendt06) for the original notebook

  - [MLo7](https://github.com/MLo7Ghinsan) for the repo's content

  - [PixPrucer](https://twitter.com/PixPrucer?s=20) for an in-depth SVS guide
    
  - [haru0l](https://x.com/mscoocoo2?s=20) for the base pretrain with embeds
