import zipfile, shutil, csv, json, yaml, random, subprocess, os, requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
from tqdm import tqdm

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("850x600")
        self.title("DiffSinger Training GUI")
        self.resizable(False, False)
        self.iconbitmap("sussy.ico")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background = "gray18", font = "Bahnschrift", bordercolor = "gray69") #gray cus i like gray since it sounds close to gay
        style.configure('TNotebook.Tab', background = "gray18", foreground = "cyan3")
        style.configure('TLabel', foreground = "cyan3")
        style.configure('TButton', background = "Cyan4", foreground = "white", bordercolor = "gray69")
        style.configure('small.TButton', font = "Bahnschrift 10")
        style.map("TNotebook.Tab", background=[("selected", "cyan4")], foreground=[("selected", "white")])
        style.configure('TCheckbutton', foreground = "Cyan3", font = "Bahnschrift 16")
        style.map("TCheckbutton", background = [("active", "gray18")])
        style.configure("TCheckbutton", indicatorbackground="gray18", indicatorforeground="cyan3")
        style.configure('TRadiobutton', foreground = "Cyan3", font = "Bahnschrift 16")
        style.map("TRadiobutton", background = [("active", "gray18")])
        style.configure("TRadiobutton", indicatorbackground="gray18", indicatorforeground="cyan3")
        self.create_widgets()

        self.all_shits = None #forcing users to select the folder <3

    def create_widgets(self):

        #Set up tabs
        tabControl = ttk.Notebook(self)
  
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        tab4 = ttk.Frame(tabControl)
        tab5 = ttk.Frame(tabControl)

        tabControl.add(tab1, text ='About')
        tabControl.add(tab2, text ='Segment & Format Data')
        tabControl.add(tab3, text ='Edit Config & Preprocess')
        tabControl.add(tab4, text ='Train Model')
        tabControl.add(tab5, text ='Build OpenUtau Voicebank')
        tabControl.pack(expand = 1, fill ="both")

        #ABOUT TAB
        tab1.label = ttk.Label(tab1, text ="DiffSinger Training GUI", font = "Bahnschrift 40 bold")
        tab1.label.pack(side = "top", pady = (200, 0))
        tab1.label = ttk.Label(tab1, text ="by MLo7 & AgentAsteriski")
        tab1.label.pack()
        tab1.label = ttk.Label(tab1, text ="updated 12/8/23", font = "Bahnschrift 10")
        tab1.label.pack()
        tab1.button = ttk.Button(tab1, text="Download dependencies", command=self.dl_scripts_github)
        tab1.button.pack()

        #SEGMENT TAB

        tab2.label = ttk.Label(tab2, text = "Max no. of silences per segment")
        tab2.label.grid(padx = (120, 0), pady = (50, 0))
        global max_sil
        max_sil = tk.StringVar()
        tab2.maxsil_box = ttk.Entry(tab2, textvariable = max_sil, width = 5)
        tab2.maxsil_box.insert(0, "2")
        tab2.maxsil_box.grid(row = 2, padx = (120, 20))
        tab2.maxsil_scale = tk.Scale(tab2, variable = max_sil, resolution = 1, from_ = 0, to = 10, orient = "horizontal", length = 150, bg = "gray18", fg = "cyan3", font = "Bahnschrift")
        tab2.maxsil_scale.grid(row = 1, padx = (120, 20))
        

        tab2.label = ttk.Label(tab2, text = "Max length of silences")
        tab2.label.grid(row = 0, column = 1, padx = (120, 20), pady = (50, 0))
        global max_sil_length
        max_sil_length = tk.StringVar(value = 0.5)
        tab2.maxsillength_scale = tk.Scale(tab2, variable = max_sil_length, resolution = "0.5", from_ = 0, to = 5, orient = "horizontal", length = 150, bg = "gray18", fg = "cyan3", font = "Bahnschrift")
        tab2.maxsillength_scale.grid(row = 1, column = 1, padx = (120, 20))
        tab2.maxsillength_box = ttk.Entry(tab2, textvariable = max_sil_length, width = 5)
        tab2.maxsillength_box.grid(row = 2, column = 1, padx = (120, 20))


        tab2.label = ttk.Label(tab2, text = "Max length of segments")
        tab2.label.grid(row = 3, pady = (25, 0), padx = (120, 20))
        global max_seg_length
        max_seg_length = tk.IntVar(value = 15)
        tab2.maxseglength_scale = tk.Scale(tab2, variable = max_seg_length, resolution = 1, from_ = 0, to = 45, orient = "horizontal", length = 150, bg = "gray18", fg = "cyan3", font = "Bahnschrift")
        tab2.maxseglength_scale.grid(row = 4, padx = (120, 20))
        tab2.maxseglength_box = ttk.Entry(tab2, textvariable = max_seg_length, width = 5)
        tab2.maxseglength_box.grid(row = 5, padx = (120, 20))


        self.estimatemidivar = tk.BooleanVar()
        tab2.estimatemidi = ttk.Checkbutton(tab2, text = "Estimate MIDI", variable = self.estimatemidivar)
        tab2.estimatemidi.grid(row = 3, column = 1, padx = (120, 20), rowspan = 2)
        global estimate_midi
        estimate_midi = self.estimatemidivar

        self.breathcheckvar = tk.BooleanVar()
        tab2.breathcheck = ttk.Checkbutton(tab2, text = "Detect breath", variable = self.breathcheckvar)
        tab2.breathcheck.grid(row = 4, column = 1, padx = (120, 20), rowspan = 2)
        global detectbreath
        detectbreath = self.breathcheckvar

        ttk.Button(tab2, text = "Select raw data folder", command = self.grab_data).grid(row = 6, columnspan = 2, pady = (25, 0), padx = (165, 20))
        ttk.Button(tab2, text = "Segment and format data", command = self.run_segment).grid(row = 7, columnspan = 2, pady = (25, 0), padx = (165, 20))

        #CONFIG TAB
        self.trainselect_option = tk.StringVar()
        tab3.option1 = ttk.Radiobutton(tab3, text="Acoustic", variable=self.trainselect_option, value="Acoustic Training")
        tab3.option1.grid(row = 0, column = 0, pady = (10, 0))
        tab3.option2 = ttk.Radiobutton(tab3, text="Variance", variable=self.trainselect_option, value="Variance Training")
        tab3.option2.grid(row = 0, column = 1, pady = (10, 0))
        global trainselect
        trainselect = self.trainselect_option

        self.shallow_var = tk.BooleanVar()
        tab3.shallowcheck = ttk.Checkbutton(tab3, text = "Use shallow diffusion", variable = self.shallow_var)
        tab3.shallowcheck.grid(row = 1, column = 0, columnspan = 2)
        global shallowdiff
        shallowdiff = self.shallow_var

        ttk.Button(tab3, text = "Select binary folder").grid(row = 2, column = 0, pady = (10, 0))
        ttk.Button(tab3, text = "Select checkpoint folder").grid(row = 2, column = 1, pady = (10, 0))

        tab3.label = ttk.Label(tab3, text = "-------------------------------------------------------------------------------").grid(row = 3, column = 0, columnspan = 2, padx = 50, pady = 5)

        tab3.label = ttk.Label(tab3, text = "Augment options").grid(row = 4, column = 0)
        self.fixedaugvar = tk.BooleanVar()
        tab3.fixedcheck = ttk.Checkbutton(tab3, text = "Fixed pitch", variable = self.fixedaugvar)
        tab3.fixedcheck.grid(row = 4, column = 1)
        self.randomaugvar = tk.BooleanVar()
        tab3.randomcheck = ttk.Checkbutton(tab3, text = "Random pitch", variable = self.randomaugvar)
        tab3.randomcheck.grid(row = 5, column = 0)
        self.stretchvar = tk.BooleanVar()
        tab3.stretchcheck = ttk.Checkbutton(tab3, text = "Time stretching", variable = self.stretchvar)
        tab3.stretchcheck.grid(row = 5, column = 1)

        tab3.label = ttk.Label(tab3, text = "-------------------------------------------------------------------------------").grid(row = 6, column = 0, columnspan = 2, padx = 50, pady = 5)

        self.train_ene_var = tk.BooleanVar()
        tab3.ene_check = ttk.Checkbutton(tab3, text = "Train energy", variable = self.train_ene_var)
        tab3.ene_check.grid(row = 7, column = 0)
        self.train_bre_var = tk.BooleanVar()
        tab3.bre_check = ttk.Checkbutton(tab3, text = "Train breathiness", variable = self.train_bre_var)
        tab3.bre_check.grid(row = 7, column = 1)
        self.train_pit_var = tk.BooleanVar()
        tab3.pit_check = ttk.Checkbutton(tab3, text = "Train pitch", variable = self.train_pit_var)
        tab3.pit_check.grid(row = 8, column = 0)
        self.train_dur_var = tk.BooleanVar()
        tab3.dur_check = ttk.Checkbutton(tab3, text = "Train duration", variable = self.train_dur_var)
        tab3.dur_check.grid(row = 8, column = 1)

        tab3.label = ttk.Label(tab3, text = "-------------------------------------------------------------------------------").grid(row = 9, column = 0, columnspan = 2, padx = 50, pady = 5)

        tab3.label = ttk.Label(tab3, text = "Save interval")
        tab3.label.grid(row = 10, column = 0)
        global save_int
        save_int = tk.StringVar()
        tab3.save_box = ttk.Entry(tab3, textvariable = save_int, width = 5)
        tab3.save_box.insert(0, "2000")
        tab3.save_box.grid(row = 12, column = 0)
        tab3.save_scale = tk.Scale(tab3, variable = save_int, resolution = 100, from_ = 1000, to = 10000, orient = "horizontal", length = 150, bg = "gray18", fg = "cyan3", font = "Bahnschrift")
        tab3.save_scale.grid(row = 11, column = 0)

        tab3.label = ttk.Label(tab3, text = "Batch size")
        tab3.label.grid(row = 10, column = 1)
        global batch_size
        batch_size = tk.StringVar()
        tab3.batch_box = ttk.Entry(tab3, textvariable = batch_size, width = 5)
        tab3.batch_box.insert(0, "9")
        tab3.batch_box.grid(row = 12, column = 1)
        tab3.batch_scale = tk.Scale(tab3, variable = batch_size, resolution = 1, from_ = 6, to = 50, orient = "horizontal", length = 150, bg = "gray18", fg = "cyan3", font = "Bahnschrift")
        tab3.batch_scale.grid(row = 11, column = 1)

        self.precision_option = tk.StringVar()
        self.option_menu = ttk.Combobox(tab3, textvariable = self.precision_option)  
        self.option_menu['values'] = ["idk", "placeholder", "values here", "i think there's 4"]
        self.option_menu['state'] = 'readonly'
        self.prec1_var = tk.BooleanVar()
        self.prec2_var = tk.BooleanVar()
        self.prec3_var = tk.BooleanVar()
        self.prec4_var = tk.BooleanVar()
        self.option_menu.grid(row = 13, column = 0, pady = (10, 0))

        self.sample_var = tk.BooleanVar()
        tab3.samplecheck = ttk.Checkbutton(tab3, text = "Randomize samples", variable = self.sample_var)
        tab3.samplecheck.grid(row = 13, column = 1)
        global randomsample
        randomsample = self.sample_var

        ttk.Button(tab3, text = "Write config").grid(row = 14, column = 0, pady = (10, 0))
        ttk.Button(tab3, text = "Binarize").grid(row = 14, column = 1, pady = (10, 0))

    ##FINAL COMMANDS
    global all_shits_not_wav_n_lab
    all_shits_not_wav_n_lab = "raw_data/diffsinger_db"

    def dl_scripts_github(self):
        if not os.path.exists(all_shits_not_wav_n_lab):
          os.makedirs(all_shits_not_wav_n_lab)
        uta_url = "https://github.com/UtaUtaUtau/nnsvs-db-converter/archive/refs/heads/main.zip"
        uta_zip = os.path.join(os.getcwd(), uta_url.split("/")[-1])  # current scripts dir to avoid issues
        uta_script_folder_name = "nnsvs-db-converter-main"

        diffsinger_url = "https://github.com/openvpi/DiffSinger/archive/refs/heads/main.zip"
        diffsinger_zip = os.path.join(os.getcwd(), diffsinger_url.split("/")[-1])  # current scripts dir to avoid issues
        diffsinger_script_folder_name = "DiffSinger-main"

        vocoder_url = "https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-v1/nsf_hifigan_20221211.zip"
        vocoder_zip = os.path.join(os.getcwd(), vocoder_url.split("/")[-1])  # current scripts dir to avoid issues
        vocoder_folder = "DiffSinger/checkpoints"


        if os.path.exists("nnsvs-db-converter") or os.path.exists("DiffSinger"):
            user_response = messagebox.askyesno("File Exists", "Necessary files already exist. Do you want to re-download and replace them?")
            if not user_response:
                return

            if os.path.exists("nnsvs-db-converter"):
                try:
                    shutil.rmtree("nnsvs-db-converter")
                except Exception as e:
                    print(f"Error deleting the existing 'nnsvs-db-converter' folder: {e}")

            if os.path.exists("DiffSinger"):
                try:
                    shutil.rmtree("DiffSinger")
                except Exception as e:
                    print(f"Error deleting the existing 'DiffSinger' folder: {e}")

        response = requests.get(uta_url, stream = True)
        total_size = int(response.headers.get("content-length", 0))
        with tqdm(total = total_size, unit = "B", unit_scale = True, desc = "downloading nnsvs-db-converter") as progress_bar:
            with open("main.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))

        with zipfile.ZipFile(uta_zip, "r") as zip_ref:
            zip_ref.extractall()
        os.remove(uta_zip)
        if os.path.exists(uta_script_folder_name):
            os.rename(uta_script_folder_name, "nnsvs-db-converter") #renaming stuff cus i dont wanna change my path from the nb much

        response = requests.get(diffsinger_url, stream = True)
        total_size = int(response.headers.get("content-length", 0))
        with tqdm(total = total_size, unit = "B", unit_scale = True, desc = "downloading DiffSinger") as progress_bar:
            with open("main.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))

        with zipfile.ZipFile(diffsinger_zip, "r") as zip_ref:
            zip_ref.extractall()
        os.remove(diffsinger_zip)
        if os.path.exists(diffsinger_script_folder_name):
            os.rename(diffsinger_script_folder_name, "DiffSinger") #this beech too

        response = requests.get(vocoder_url, stream = True)
        total_size = int(response.headers.get("content-length", 0))
        with tqdm(total = total_size, unit = "B", unit_scale = True, desc = "downloading NSF-HifiGAN") as progress_bar:
            with open("nsf_hifigan_20221211.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
        with zipfile.ZipFile(vocoder_zip, "r") as zip_ref:
            zip_ref.extractall(vocoder_folder)
        os.remove(vocoder_zip)

        subprocess.check_call(["pip", "install", "-r", "DiffSinger/requirements.txt"])
        subprocess.check_call(["pip", "install", "torch==1.13.0"])
        subprocess.check_call(["pip", "install", "torchvision==0.14.0"])
        subprocess.check_call(["pip", "install", "torchaudio==0.13.0"])
        subprocess.check_call(["pip", "install", "protobuf"])
        subprocess.check_call(["pip", "install", "onnxruntime"])

        if os.path.exists("db_converter_config.yaml"):
            os.remove("db_converter_config.yaml")

        converter_config = {
            "use_cents": False,
            "time_step": 0.005,
            "f0_min": 40,
            "f0_max": 1100,
            "voicing_treshold_midi": 0.45,
            "voicing_treshold_breath": 0.6,
            "breath_window_size": 0.05,
            "breath_min_length": 0.1,
            "breath_db_threshold": -60,
            "breath_centroid_treshold": 2000,
            "write_label": "htk"
        }
        with open("db_converter_config.yaml", "w") as config:
            yaml.dump(converter_config, config)

        print("Setup Complete!")


    def grab_data(self):
        self.all_shits = filedialog.askdirectory(title="Select raw data folder", initialdir = "raw_data")
        print("raw data path: " + self.all_shits)

        
    def run_segment(self):
        if self.all_shits is None:
            messagebox.showinfo("Required", "Please selecta a folder containing raw data folder(s) first")
            return
        messagebox.showinfo("Warning", 'This process will remove the original .wav and .lab files, please be sure to make a backup for your data before pressing "OK" or closing this window')
        print("\n")
        print("process running...")
        print("editing necessary phonemes for db converter...")
        # incase if user labeled SP as pau but i think utas script already account SP so meh
        for root, dirs, files in os.walk(self.all_shits):
            for filename in files:
                if filename.endswith(".lab"):
                    file_path = os.path.join(root, filename)
                    with open(file_path, "r") as file:
                        file_data = file.read()
                    file_data = file_data.replace("SP", "pau")
                    file_data = file_data.replace("br", "AP") #it needs AP instead of br, but if users didnt label breath then whoop their lost
                    with open(file_path, "w") as file:
                        file.write(file_data)
        # for funny auto dict generator lmao
        print("generating dictionary from phonemes...")
        out = "DiffSinger/dictionaries/custom_dict.txt"

        phonemes = set()

        def is_excluded(phoneme):
            return phoneme in ["pau", "AP", "SP", "sil"]

        phoneme_folder_path = self.all_shits
        for root, dirs, files in os.walk(phoneme_folder_path):
            for file in files:
                if file.endswith(".lab"):
                    fpath = os.path.join(root, file)
                    with open(fpath, "r") as lab_file:
                        for line in lab_file:
                            line = line.strip()
                            if line:
                                phoneme = line.split()[2]
                                if not is_excluded(phoneme):
                                    phonemes.add(phoneme)
        phoneme_folder_path = all_shits_not_wav_n_lab
        for root, dirs, files in os.walk(phoneme_folder_path):
            for file in files:
                if file.endswith(".csv"):
                    fpath = os.path.join(root, file)
                    with open(fpath, "r", newline="") as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        for row in csv_reader:
                            if "ph_seq" in row:
                                ph_seq = row["ph_seq"].strip()
                                for phoneme in ph_seq.split():
                                    if not is_excluded(phoneme):
                                        phonemes.add(phoneme)
        phoneme_folder_path = self.all_shits
        for root, dirs, files in os.walk(phoneme_folder_path):
            for file in files:
                if file.endswith(".json"):
                    fpath = os.path.join(root, file)
                    with open(fpath, "r") as json_file:
                        row = json.load(json_file)
                        ph_seq = row["ph_seq"]
                        for phoneme in ph_seq.split():
                            if not is_excluded(phoneme):
                                phonemes.add(phoneme)

        with open(out, "w") as f:
            for phoneme in sorted(phonemes):
                f.write(phoneme + "	" + phoneme + "\n")

        # for vowels and consonants.txt.... well adding luquid type for uta's script
        dict_path = out
        vowel_types = {"a", "i", "u", "e", "o", "N", "M", "NG"}
        liquid_types = {"y", "w", "l", "r"} # r for english labels, it should be fine with jp too
        vowel_data = []
        consonant_data = []
        liquid_data = []

        with open(dict_path, "r") as f:
            for line in f:
                phoneme, _ = line.strip().split("\t")
                if phoneme[0] in vowel_types:
                    vowel_data.append(phoneme)
                elif phoneme[0] in liquid_types:
                    liquid_data.append(phoneme)
                else:
                    consonant_data.append(phoneme)

        vowel_data.sort()
        liquid_data.sort()
        consonant_data.sort()
        directory = os.path.dirname(dict_path)

        # make txt for language json file
        print("writing vowels.txt...")
        vowel_txt_path = os.path.join(directory, "vowels.txt")
        with open(vowel_txt_path, "w") as f:
            f.write(" ".join(vowel_data))
        print("writing liquids.txt...")
        liquid_txt_path = os.path.join(directory, "liquids.txt")
        with open(liquid_txt_path, "w") as f:
            f.write(" ".join(liquid_data))
        print("writing consonants.txt...")
        consonant_txt_path = os.path.join(directory, "consonants.txt")
        with open(consonant_txt_path, "w") as f:
            f.write(" ".join(consonant_data))

        # here's a funny json append
        print("appending lang.sample.json...")
        with open(vowel_txt_path, "r") as f:
            vowel_data = f.read().split()
        with open(liquid_txt_path, "r") as f:
            liquid_data = f.read().split()
        with open(consonant_txt_path, "r") as f:
            consonant_data = f.read().split()
        phones4json = {"vowels": vowel_data, "liquids": liquid_data}
        with open("nnsvs-db-converter/lang.sample.json", "w") as rawr:
            json.dump(phones4json, rawr, indent=4)

        with open("db_converter_config.yaml", "r") as config:
            converter = yaml.safe_load(config)

        max_silence = max_sil.get()
        max_silence_length = max_sil_length.get()
        max_wav_length = max_seg_length.get()
        
        for raw_folder_name in os.listdir(self.all_shits):
            raw_folder_path = os.path.join(self.all_shits, raw_folder_name)
            if any(filename.endswith(".lab") for filename in os.listdir(raw_folder_path)):
                print("segmenting data...")
                #dear god please work
                cmd = ['python', 'nnsvs-db-converter\db_converter.py', '-l', str(max_wav_length), '-s', str(max_silence), '-S', str(max_silence_length), '-L', 'nnsvs-db-converter/lang.sample.json', '-F', '1600', "--folder", raw_folder_path]
                if self.estimatemidivar.get() == True:
                    cmd.append('-mD')
                    cmd.append('-f')
                    cmd.append(str(converter["f0_min"]))
                    cmd.append('-F')
                    cmd.append(str(converter["f0_max"]))
                    cmd.append("-V")
                    cmd.append(str(converter["voicing_treshold_midi"]))
                    estimate_midi_print = "True"
                else:
                    estimate_midi_print = "False"
                if converter["use_cents"] == True:
                    cmd.append("-c")
                    use_cents_print = "True"
                else:
                    use_cents_print = "False"
                if self.breathcheckvar.get() == True:
                    cmd.append('-B')
                    cmd.append("-v")
                    cmd.append(str(converter["voicing_treshold_breath"]))
                    cmd.append("-W")
                    cmd.append(str(converter["breath_window_size"]))
                    cmd.append("-b")
                    cmd.append(str(converter["breath_min_length"]))
                    cmd.append("-e")
                    cmd.append(str(converter["breath_db_threshold"]))
                    cmd.append("-C")
                    cmd.append(str(converter["breath_centroid_treshold"]))
                    detect_breath_print = "True"
                else:
                    detect_breath_print = "False"
                if converter["write_label"] == False:
                    write_label_print = "Not writing labels"
                elif converter["write_label"] == "htk":
                    cmd.append("-w htk")
                    write_label_print = "Write HTK labels"
                elif converter["write_label"] == "aud":
                    cmd.append("-w aud")
                    write_label_print = "Write Audacity labels"
                else:
                    write_label_print = "unknown value, not writing labels"
                print("\n",
                    "##### Converter Settings #####\n",
                    f"max audio segment length: {str(max_wav_length)}\n",
                    f"max silence amount: {str(max_silence)}\n",
                    f"max silence length: {str(max_silence_length)}\n",
                    f"estimate midi: {estimate_midi_print}\n",
                    f"detect off cents: {use_cents_print}\n",
                    f"detect breath: {detect_breath_print}\n",
                    f"export label: {write_label_print}\n"
                     )


                output = subprocess.check_output(cmd, universal_newlines=True)
                print(output)

                #this for folder organization / raw data cleanup
                for filename in os.listdir(raw_folder_path):
                    if filename.endswith(".wav") or filename.endswith(".lab"):
                        os.remove(os.path.join(raw_folder_path, filename))
                diff_singer_db_path = os.path.join(raw_folder_path, "diffsinger_db")
                for stuff in os.listdir(diff_singer_db_path):
                    stuff_path = os.path.join(diff_singer_db_path, stuff)
                    singer_folder_dat_main = os.path.join(raw_folder_path, stuff)
                    if os.path.isfile(stuff_path):
                        shutil.move(stuff_path, singer_folder_dat_main)
                    elif os.path.isdir(stuff_path):
                        shutil.move(stuff_path, singer_folder_dat_main)
                shutil.rmtree(diff_singer_db_path)
        print("data segmentation complete!")
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
