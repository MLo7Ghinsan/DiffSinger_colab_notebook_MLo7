import zipfile, shutil, csv, json, yaml, random, subprocess, os, requests, re
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
        style.map("TCombobox", background = [("active", "gray18")])
        style.configure("TCombobox", darkcolor = "gray18", bordercolor = "gray18", focusfill = "gray18", fieldbackground = "gray18", insertcolor = "gray18", selectbackground="gray18", selectforeground="cyan3", background="gray18", foreground="cyan3")
        self.create_widgets()

        main_path = os.getcwd()
        os.chdir(main_path)

        self.all_shits = None #forcing users to select the folder <3
        self.data_folder = None #more forces
        self.ckpt_save_dir = None #even more forces
        self.trainselect_option = None #rawr

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
        tab1.label = ttk.Label(tab1, text ="updated 2/19/24", font = "Bahnschrift 10")
        tab1.label.pack()
        tab1.button = ttk.Button(tab1, text="Full download(no CUDA)", command=self.dl_scripts_github)
        tab1.button.pack()
        tab1.button = ttk.Button(tab1, text="Full download(yes CUDA)", command=self.dl_scripts_github2)
        tab1.button.pack()
        tab1.button = ttk.Button(tab1, text="Update DS/Segmenter", command=self.dl_update)
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
        tab2.maxsillength_scale = tk.Scale(tab2, variable = max_sil_length, resolution = "0.25", from_ = 0, to = 10, orient = "horizontal", length = 150, bg = "gray18", fg = "cyan3", font = "Bahnschrift")
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

        ttk.Button(tab2, text = "Select raw data folder", command = self.grab_raw_data).grid(row = 6, columnspan = 2, pady = (25, 0), padx = (165, 20))
        ttk.Button(tab2, text = "Segment and format data", command = self.run_segment).grid(row = 7, columnspan = 2, pady = (25, 0), padx = (165, 20))

        #CONFIG TAB
        self.trainselect_option = tk.StringVar()
        tab3.option1 = ttk.Radiobutton(tab3, text="Acoustic", variable=self.trainselect_option, value="Acoustic Training")
        tab3.option1.grid(row = 0, column = 0, pady = (10, 0))
        tab3.option2 = ttk.Radiobutton(tab3, text="Variance", variable=self.trainselect_option, value="Variance Training")
        tab3.option2.grid(row = 0, column = 1, pady = (10, 0))
        global trainselect
        trainselect = self.trainselect_option

        ttk.Button(tab3, text = "Select data folder", command = self.grab_data_folder).grid(row = 2, column = 0, pady = (10, 0))
        ttk.Button(tab3, text = "Select save folder", command = self.ckpt_folder_save).grid(row = 2, column = 1, pady = (10, 0))

        tab3.label = ttk.Label(tab3, text = "-------------------------------------------------------------------------------").grid(row = 3, column = 0, columnspan = 2, padx = 50, pady = 5)

        tab3.label = ttk.Label(tab3, text = "Augment options").grid(row = 4, column = 0)
        self.fixedaugvar = tk.BooleanVar()
        tab3.fixedcheck = ttk.Checkbutton(tab3, text = "Fixed pitch", variable = self.fixedaugvar)
        tab3.fixedcheck.grid(row = 4, column = 1)
        global fixedaug
        fixedaug = self.fixedaugvar
        self.randomaugvar = tk.BooleanVar()
        tab3.randomcheck = ttk.Checkbutton(tab3, text = "Random pitch", variable = self.randomaugvar)
        tab3.randomcheck.grid(row = 5, column = 0)
        global randomaug
        randomaug = self.randomaugvar
        self.stretchvar = tk.BooleanVar()
        tab3.stretchcheck = ttk.Checkbutton(tab3, text = "Time stretching", variable = self.stretchvar)
        tab3.stretchcheck.grid(row = 5, column = 1)
        global stretchaug
        stretchaug = self.stretchvar

        tab3.label = ttk.Label(tab3, text = "-------------------------------------------------------------------------------").grid(row = 6, column = 0, columnspan = 2, padx = 50, pady = 5)

        self.train_ene_var = tk.BooleanVar()
        tab3.ene_check = ttk.Checkbutton(tab3, text = "Train energy/breath", variable = self.train_ene_var)
        tab3.ene_check.grid(row = 7, column = 0)
        global train_energy
        train_energy = self.train_ene_var
        self.train_ten_var = tk.BooleanVar()
        tab3.ten_check = ttk.Checkbutton(tab3, text = "Train tension", variable = self.train_ten_var)
        tab3.ten_check.grid(row = 7, column = 1)
        global train_ten
        train_ten = self.train_ten_var
        self.train_pit_var = tk.BooleanVar()
        tab3.pit_check = ttk.Checkbutton(tab3, text = "Train pitch", variable = self.train_pit_var)
        tab3.pit_check.grid(row = 8, column = 0)
        global train_pitch
        train_pitch = self.train_pit_var
        self.train_dur_var = tk.BooleanVar()
        tab3.dur_check = ttk.Checkbutton(tab3, text = "Train duration", variable = self.train_dur_var)
        tab3.dur_check.grid(row = 8, column = 1)
        global train_dur
        train_dur = self.train_dur_var

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
        self.option_menu['values'] = ["32-true", "bf16-mixed", "16-mixed", "bf16", "16"]
        self.option_menu['state'] = 'readonly'
        self.option_menu.grid(row = 13, column = 0, pady = (10, 0))

        self.shallow_var = tk.BooleanVar()
        tab3.shallowcheck = ttk.Checkbutton(tab3, text = "Use shallow diffusion", variable = self.shallow_var)
        tab3.shallowcheck.grid(row = 13, column = 1)
        global shallow_diff
        shallow_diff = self.shallow_var

        ttk.Button(tab3, text = "Write config", command = self.write_config).grid(row = 14, column = 0, pady = (10, 0))
        ttk.Button(tab3, text = "Binarize", command = self.binarize).grid(row = 14, column = 1, pady = (10, 0))

        #TRAINING TAB
        ttk.Button(tab4, text = "Select config", command = self.load_config_function).grid(row = 0, column = 0, padx = (175, 100), pady = (50, 50))
        ttk.Button(tab4, text = "Select save folder", command = self.ckpt_folder_save).grid(row = 0, column = 1, padx = (100, 175), pady = (50, 50))
        ttk.Button(tab4, text = "Train!", command = self.train_function).grid(row = 1, column = 0, columnspan = 2)
        ttk.Label(tab4, text = "This window will not respond during training.").grid(row = 2, column = 0, columnspan = 2, pady = (50, 5))
        ttk.Label(tab4, text = "To stop training, press Ctrl+C in the command line window.").grid(row = 3, column = 0, columnspan = 2, pady = 5)
        
        #EXPORT TAB
        self.expselect_option = tk.StringVar()
        tab5.option1 = ttk.Radiobutton(tab5, text="Acoustic", variable=self.expselect_option, value="acoustic")
        tab5.option1.grid(row = 1, column = 0, padx = (50, 0), pady = (10, 0))
        tab5.option2 = ttk.Radiobutton(tab5, text="Variance", variable=self.expselect_option, value="variance")
        tab5.option2.grid(row = 1, column = 1, pady = (10, 0))
        global expselect
        expselect = self.expselect_option
        ttk.Button(tab5, text = "Select checkpoint folder", command = self.ckpt_folder_save).grid(row = 1, column = 2, columnspan = 2, padx = (50, 0), pady = (10, 0))
        ttk.Button(tab5, text = "Select export folder", command = self.onnx_folder_save).grid(row = 1, column = 4, columnspan = 2, padx = (50, 0), pady = (10, 0))
        global onnx_folder
        onnx_folder = self.onnx_folder_save
        ttk.Button(tab5, text = "Export onnx", command = self.run_onnx_export).grid(row = 2, column = 2, columnspan = 3, pady = (10, 0))
        ttk.Label(tab5, text = "THIS TAB DOESN'T WORK YET").grid(row = 3, column = 1, padx = 10, pady = 10)



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

        vocoder_url = "https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-44.1k-hop512-128bin-2024.02/nsf_hifigan_44.1k_hop512_128bin_2024.02.zip"
        vocoder_zip = os.path.join(os.getcwd(), vocoder_url.split("/")[-1])  # current scripts dir to avoid issues
        vocoder_folder = "DiffSinger/checkpoints"
        vocoder_subfolder_name = "Diffsinger/checkpoints/nsf_hifigan_44.1k_hop512_128bin_2024.02"


        if os.path.exists("nnsvs-db-converter") or os.path.exists("DiffSinger"):
            user_response = messagebox.askyesno("File Exists", "Necessary files already exist. Do you want to re-download and replace them? Make sure any user files are backed up OUTSIDE of the Diffsinger folder.")
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
            with open("nsf_hifigan_44.1k_hop512_128bin_2024.02.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
        with zipfile.ZipFile(vocoder_zip, "r") as zip_ref:
            zip_ref.extractall(vocoder_folder)
        os.remove(vocoder_zip)
        if os.path.exists(vocoder_subfolder_name):
            os.rename(vocoder_subfolder_name, "Diffsinger/checkpoints/nsf_hifigan")

        subprocess.check_call(["pip", "install", "-r", "DiffSinger/requirements.txt"])
        subprocess.check_call(["pip", "install", "torch==1.13.0"])
        subprocess.check_call(["pip", "install", "torchvision==0.14.0"])
        subprocess.check_call(["pip", "install", "torchaudio==0.13.0"])
        subprocess.check_call(["pip", "install", "protobuf"])
        subprocess.check_call(["pip", "install", "onnxruntime"])

        if os.path.exists("db_converter_config.yaml"):
            os.remove("db_converter_config.yaml")

        converter_config = {
            "use_cents": True,
            "time_step": 0.005,
            "f0_min": 40,
            "f0_max": 1200,
            "audio_sample_rate": 44100,
            "voicing_treshold_midi": 0.45,
            "voicing_treshold_breath": 0.6,
            "breath_window_size": 0.05,
            "breath_min_length": 0.1,
            "breath_db_threshold": -60,
            "breath_centroid_treshold": 2000,
            "max-length-relaxation-factor": 0.1,
            "pitch-extractor": "parselmouth",
            "write_label": "htk"
        }
        with open("db_converter_config.yaml", "w") as config:
            yaml.dump(converter_config, config)

        print("Setup Complete!")

    def dl_scripts_github2(self):
        if not os.path.exists(all_shits_not_wav_n_lab):
          os.makedirs(all_shits_not_wav_n_lab)
        uta_url = "https://github.com/UtaUtaUtau/nnsvs-db-converter/archive/refs/heads/main.zip"
        uta_zip = os.path.join(os.getcwd(), uta_url.split("/")[-1])  # current scripts dir to avoid issues
        uta_script_folder_name = "nnsvs-db-converter-main"

        diffsinger_url = "https://github.com/openvpi/DiffSinger/archive/refs/heads/main.zip"
        diffsinger_zip = os.path.join(os.getcwd(), diffsinger_url.split("/")[-1])  # current scripts dir to avoid issues
        diffsinger_script_folder_name = "DiffSinger-main"

        vocoder_url = "https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-44.1k-hop512-128bin-2024.02/nsf_hifigan_44.1k_hop512_128bin_2024.02.zip"
        vocoder_zip = os.path.join(os.getcwd(), vocoder_url.split("/")[-1])  # current scripts dir to avoid issues
        vocoder_folder = "DiffSinger/checkpoints"
        vocoder_subfolder_name = "Diffsinger/checkpoints/nsf_hifigan_44.1k_hop512_128bin_2024.02"


        if os.path.exists("nnsvs-db-converter") or os.path.exists("DiffSinger"):
            user_response = messagebox.askyesno("File Exists", "Necessary files already exist. Do you want to re-download and replace them? Make sure any user files are backed up OUTSIDE of the Diffsinger folder.")
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
            with open("nsf_hifigan_44.1k_hop512_128bin_2024.02.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
        with zipfile.ZipFile(vocoder_zip, "r") as zip_ref:
            zip_ref.extractall(vocoder_folder)
        os.remove(vocoder_zip)
        if os.path.exists(vocoder_subfolder_name):
            os.rename(vocoder_subfolder_name, "Diffsinger/checkpoints/nsf_hifigan")
        

        subprocess.check_call(["pip", "install", "-r", "DiffSinger/requirements.txt"])
        subprocess.check_call(["pip", "install", "torch==1.13.1+cu117", "torchvision==0.14.1+cu117", "torchaudio==0.13.1", "--extra-index-url", "https://download.pytorch.org/whl/cu117"])
        subprocess.check_call(["pip", "install", "protobuf"])
        subprocess.check_call(["pip", "install", "onnxruntime"])

        if os.path.exists("db_converter_config.yaml"):
            os.remove("db_converter_config.yaml")

        converter_config = {
            "use_cents": True,
            "time_step": 0.005,
            "f0_min": 40,
            "f0_max": 1200,
            "audio_sample_rate": 44100,
            "voicing_treshold_midi": 0.45,
            "voicing_treshold_breath": 0.6,
            "breath_window_size": 0.05,
            "breath_min_length": 0.1,
            "breath_db_threshold": -60,
            "breath_centroid_treshold": 2000,
            "max-length-relaxation-factor": 0.1,
            "pitch-extractor": "parselmouth",
            "write_label": "htk"
        }
        with open("db_converter_config.yaml", "w") as config:
            yaml.dump(converter_config, config)

        print("Setup Complete!")

    def dl_update(self):
        if not os.path.exists(all_shits_not_wav_n_lab):
          os.makedirs(all_shits_not_wav_n_lab)
        uta_url = "https://github.com/UtaUtaUtau/nnsvs-db-converter/archive/refs/heads/main.zip"
        uta_zip = os.path.join(os.getcwd(), uta_url.split("/")[-1])  # current scripts dir to avoid issues
        uta_script_folder_name = "nnsvs-db-converter-main"

        diffsinger_url = "https://github.com/openvpi/DiffSinger/archive/refs/heads/main.zip"
        diffsinger_zip = os.path.join(os.getcwd(), diffsinger_url.split("/")[-1])  # current scripts dir to avoid issues
        diffsinger_script_folder_name = "DiffSinger-main"

        vocoder_url = "https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-44.1k-hop512-128bin-2024.02/nsf_hifigan_44.1k_hop512_128bin_2024.02.zip"
        vocoder_zip = os.path.join(os.getcwd(), vocoder_url.split("/")[-1])  # current scripts dir to avoid issues
        vocoder_folder = "DiffSinger/checkpoints"
        vocoder_subfolder_name = "Diffsinger/checkpoints/nsf_hifigan_44.1k_hop512_128bin_2024.02"


        if os.path.exists("nnsvs-db-converter") or os.path.exists("DiffSinger"):
            user_response = messagebox.askyesno("File Exists", "Necessary files already exist. Do you want to re-download and replace them? Make sure any user files are backed up OUTSIDE of the Diffsinger folder.")
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
            with open("nsf_hifigan_44.1k_hop512_128bin_2024.02.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
        with zipfile.ZipFile(vocoder_zip, "r") as zip_ref:
            zip_ref.extractall(vocoder_folder)
        os.remove(vocoder_zip)
        if os.path.exists(vocoder_subfolder_name):
            os.rename(vocoder_subfolder_name, "Diffsinger/checkpoints/nsf_hifigan")


        if os.path.exists("db_converter_config.yaml"):
            os.remove("db_converter_config.yaml")

        converter_config = {
            "use_cents": True,
            "time_step": 0.005,
            "f0_min": 40,
            "f0_max": 1200,
            "audio_sample_rate": 44100,
            "voicing_treshold_midi": 0.45,
            "voicing_treshold_breath": 0.6,
            "breath_window_size": 0.05,
            "breath_min_length": 0.1,
            "breath_db_threshold": -60,
            "breath_centroid_treshold": 2000,
            "max-length-relaxation-factor": 0.1,
            "pitch-extractor": "parselmouth",
            "write_label": "htk"
        }
        with open("db_converter_config.yaml", "w") as config:
            yaml.dump(converter_config, config)

        print("Setup Complete!")

    def grab_raw_data(self):
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

    def grab_data_folder(self):
        self.data_folder = filedialog.askdirectory(title="Select data folder", initialdir = "DiffSinger")
        print("data path: " + self.data_folder)

    def ckpt_folder_save(self):
        global ckpt_save_dir
        ckpt_save_dir = filedialog.askdirectory(title="Select save folder", initialdir = "DiffSinger/checkpoints")
        self.binary_save_dir = ckpt_save_dir + "/binary"
        print("save path: " + ckpt_save_dir)
        
    def write_config(self):
        #adding checks lmao make sure they select them
        config_check = trainselect.get()
        if not config_check:
            messagebox.showinfo("Required", "Please select a config type")
            return
        if self.data_folder is None:
            messagebox.showinfo("Required", "Please select a folder containing data folder(s)")
            return
        if ckpt_save_dir is None:
            messagebox.showinfo("Required", "Please select a save directory")
            return
        print("writing config...")
        spk_name = [folder_name for folder_name in os.listdir(self.data_folder) if os.path.isdir(os.path.join(self.data_folder, folder_name))]
        # i used spk_name for something else cus i forgor now imma just copy and paste it
        spk_names = [folder_name for folder_name in os.listdir(self.data_folder) if os.path.isdir(os.path.join(self.data_folder, folder_name))]
        num_spk = len(spk_name)
        raw_dir = []
        for folder_name in spk_name:
            folder_path = os.path.join(self.data_folder, folder_name)
            raw_dir.append(folder_path)
        if num_spk == 1:
            singer_type = "SINGLE-SPEAKER"
            diff_loss_type = "l2"
            f0_emb = "continuous"
            use_spk_id = False
            all_wav_files = []
            for root, dirs, files in os.walk(self.data_folder):
                for file in files:
                    if file.endswith(".wav"):
                        full_path = os.path.join(root, file)
                        all_wav_files.append(full_path)
            random.shuffle(all_wav_files)
            random_ass_wavs = all_wav_files[:3]
            random_ass_test_files = [os.path.splitext(os.path.basename(file))[0] for file in random_ass_wavs]

        else:
            singer_type = "MULTI-SPEAKER"
            diff_loss_type = "l1"
            f0_emb = "discrete"
            use_spk_id = True
            folder_to_id = {folder_name: i for i, folder_name in enumerate(spk_name)}
            random_ass_test_files = []
            for folder_path in raw_dir:
                audio_files = [f[:-4] for f in os.listdir(folder_path + "/wavs") if f.endswith(".wav")]
                folder_name = os.path.basename(folder_path)
                folder_id = folder_to_id.get(folder_name, -1)
                prefixed_audio_files = [f"{folder_id}:{audio_file}" for audio_file in audio_files]
                random_ass_test_files.extend(prefixed_audio_files[:3])
        spk_id = []
        for i, spk_name in enumerate(spk_name):
            spk_id_format = f"{i}:{spk_name}"
            spk_id.append(spk_id_format)

 # commenting this out bc its pointless, tbh it doesnt even needs its own def, just include it with write_config or sumn
 # you can remove this btw if you feel like it, if not then i can come back to it later
 #       def update_precision(selected_value):
 #           with open("DiffSinger/configs/base.yaml", "r") as config:
 #               config_data = yaml.safe_load(config)
 #           config_data["pl_trainer_precision"] = precision.get()
 #           with open("DiffSinger/configs/base.yaml", "w") as config:
 #               yaml.dump(config_data, config)

 #       def update_config():   <----- this is not really needed
        enable_fixed_aug = fixedaug.get()
        enable_random_aug = randomaug.get()
        enable_stretch_aug = stretchaug.get()
        energy = train_energy.get()
        pitch = train_pitch.get()
        tension = train_ten.get()
        duration = train_dur.get()
        shallow = shallow_diff.get()
        save_interval = save_int.get()
        batch = batch_size.get()
        selected_config_type = trainselect.get()
        if selected_config_type == "Acoustic Training":
            with open("DiffSinger/configs/acoustic.yaml", "r") as config:
                bitch_ass_config = yaml.safe_load(config)
            bitch_ass_config["speakers"] = spk_names
            bitch_ass_config["test_prefixes"] = random_ass_test_files
            bitch_ass_config["raw_data_dir"] = raw_dir
            bitch_ass_config["num_spk"] = num_spk
            bitch_ass_config["use_spk_id"] = use_spk_id
            #bitch_ass_config["spk_ids"] = spk_id
            bitch_ass_config["diff_loss_type"] = diff_loss_type
            bitch_ass_config["f0_embed_type"] = f0_emb
            bitch_ass_config["binary_data_dir"] = self.binary_save_dir
            bitch_ass_config["dictionary"] = "dictionaries/custom_dict.txt"
            bitch_ass_config["augmentation_args"]["fixed_pitch_shifting"]["enabled"] = enable_fixed_aug
            bitch_ass_config["augmentation_args"]["random_pitch_shifting"]["enabled"] = enable_random_aug
            bitch_ass_config["augmentation_args"]["random_time_stretching"]["enabled"] = enable_stretch_aug
            bitch_ass_config["use_key_shift_embed"] = enable_random_aug
            bitch_ass_config["use_speed_embed"] = enable_stretch_aug
            bitch_ass_config["max_batch_size"] = int(batch)
            #ive never tried reaching the limit so ill trust kei's setting for this(MLo7)
            #sounds like a lot of users can go higher but 9 is a good start(Aster)
            bitch_ass_config["val_check_interval"] = int(save_interval)
            bitch_ass_config["use_energy_embed"] = energy
            bitch_ass_config["use_breathiness_embed"] = energy
            bitch_ass_config["use_tension_embed"] = tension
            #shallow diff stuff
            bitch_ass_config["use_shallow_diffusion"] = shallow
            bitch_ass_config["shallow_diffusion_args"]["val_gt_start"] = shallow
            with open("DiffSinger/configs/acoustic.yaml", "w") as config:
                yaml.dump(bitch_ass_config, config)
            print("wrote acoustic config!")

        else:
            with open("DiffSinger/configs/variance.yaml", "r") as config:
                bitch_ass_config = yaml.safe_load(config)
            bitch_ass_config["speakers"] = spk_names
            bitch_ass_config["test_prefixes"] = random_ass_test_files
            bitch_ass_config["raw_data_dir"] = raw_dir
            bitch_ass_config["num_spk"] = num_spk
            bitch_ass_config["use_spk_id"] = use_spk_id
            bitch_ass_config["diff_loss_type"] = diff_loss_type
            bitch_ass_config["binary_data_dir"] = self.binary_save_dir
            bitch_ass_config["dictionary"] = "dictionaries/custom_dict.txt"
            bitch_ass_config["max_batch_size"] = int(batch) #ive never tried reaching the limit so ill trust kei's setting for this
            bitch_ass_config["val_check_interval"] = int(save_interval)
            bitch_ass_config["predict_energy"] = energy
            bitch_ass_config["predict_breathiness"] = energy
            bitch_ass_config["predict_pitch"] = pitch
            bitch_ass_config["predict_dur"] = duration
            with open("DiffSinger/configs/variance.yaml", "w") as config:
                yaml.dump(bitch_ass_config, config)
            print("wrote variance config!")

        new_f0_max=1600
        with open("DiffSinger/utils/binarizer_utils.py", "r") as f:
            f0_read = f.read()
        up_f0_val = re.sub(r"f0_max\s*=\s*.*", f"f0_max={new_f0_max},", f0_read)
        with open("DiffSinger/utils/binarizer_utils.py", "w") as f:
            f.write(up_f0_val)

    def binarize(self):
        os.chdir("DiffSinger")
        os.environ["PYTHONPATH"] = "."
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        config_check = trainselect.get()
        cmd = ['python', 'scripts/binarize.py', '--config']
        if config_check == "Acoustic Training":
            print("binarizing acoustic...")
            cmd.append('configs/acoustic.yaml')
        elif config_check == "Variance Training":
            print("binarizing variance...")
            cmd.append('configs/variance.yaml')
        else:
            messagebox.showinfo("Required", "Please select a config type")
            return
        print(' '.join(cmd))
        output = subprocess.check_output(cmd, universal_newlines=True)
        print(output)
        os.chdir(main_path)

    def load_config_function(self):
        global configpath
        configpath = filedialog.askopenfilename(title="Select config file", initialdir="DiffSinger/configs/", filetypes=[("Config files", "*.yaml")])
        print(configpath)

    def train_function(self):
        os.chdir("DiffSinger")
        os.environ["PYTHONPATH"] = "."
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        if not configpath or not ckpt_save_dir:
            self.label.config(text="Please select your config and the data you would like to train first!")
            return
        subprocess.check_call(['python', 'scripts/train.py', '--config', configpath, '--exp_name', ckpt_save_dir, '--reset'])

    def onnx_folder_save(self):
        global onnx_folder_dir
        onnx_folder_dir = filedialog.askdirectory(title="Select onnx export folder", initialdir = "DiffSinger")
        print("export path: " + onnx_folder_dir)

    def run_onnx_export(self):
        os.chdir("DiffSinger")
        os.environ["PYTHONPATH"] = "."
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        if not onnx_folder_dir or not ckpt_save_dir:
            self.label.config(text="Please select your config and the data you would like to preprocess first!")
            return
        export_check = expselect.get()
        cmd = ['python', 'scripts/export.py']
        if export_check == "acoustic":
            print("exporting acoustic...")
            cmd.append('acoustic')
        elif export_check == "variance":
            print("exporting variance...")
            cmd.append('variance')
        else:
            messagebox.showinfo("Required", "Please select a config type")
            return
        cmd.append(['--exp', ckpt_save_dir, '--out', onnx_folder_dir])
        streeng = ' '.join([str(cmd)])
        print(streeng)
        output = subprocess.check_output(streeng, universal_newlines=True)
        print(output)
        os.chdir(main_path)
if __name__ == "__main__":
    app = App()
    app.mainloop()
