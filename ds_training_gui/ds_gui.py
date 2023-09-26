import zipfile, shutil, csv, json, yaml, random, subprocess, os, requests
from tkinter import Menu, messagebox, filedialog
from tqdm import tqdm
import tkinter as tk


window = tk.Tk()
window.title("DiffSinger Training GUI")
window.geometry("780x600")
window.configure(bg = "#3B3B3B") #gray cus i like gray since it sounds close to gay
window.resizable(False, False)
window.iconbitmap("sussy.ico")
menubar = Menu(window)
window.config(menu = menubar)

fg = "#00ECFE"
bg = "#3B3B3B"

main_path = os.getcwd()
os.chdir(main_path)

# text screen so it's not too empty
main_screen_txt = tk.Label(window, text = "DiffSinger Training GUI", font = ("Helvetica", 50), bg = bg, fg = fg)
main_screen_txt.pack(side = "top", pady = (225, 0))  # Add top padding
rawr_txt = tk.Label(window, text = "idk what to put here so the main page doesn't look too empty", font = ("Helvetica", 10), bg = bg, fg = fg)
rawr_txt.pack(side = "top", pady = (20, 0))

all_shits = "raw_data"
all_shits_not_wav_n_lab = "raw_data/diffsinger_db"

max_silence = 2
max_silence_length = 0.5
max_wav_length = 15

binary_save_dir = tk.StringVar()
energy_training = tk.StringVar()
breathiness_training = tk.StringVar()
pitch_training = tk.StringVar()
duration_training = tk.StringVar()
config_type = tk.StringVar()
use_shallow_diffusion = tk.StringVar()
precision = tk.StringVar()
data_aug = tk.StringVar()
save_interval = 2000
model_save_dir = tk.StringVar()

config_file_path = tk.StringVar()
model_save_path = tk.StringVar()

def clear_screen(window):
    widgets = window.winfo_children()
    for widget in widgets:
        if isinstance(widget, tk.Menu):
            continue
        widget.pack_forget()

def dl_scripts_github():
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

def segment_screen():
    clear_screen(window)
    os.chdir(main_path)
    main_screen_txt.pack_forget()
    rawr_txt.pack_forget()

    #===SIDE===#
    right_frame = tk.Frame(window, bg = "#4B4B4B", width = 250)
    right_frame.pack(side = "right", fill = "both", expand = False)
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    def run_segment():
        print("process running...")
        print("edit necessary phonemes for db converter...")
        # incase if user labeled SP as pau but i think utas script already account SP so meh
        for root, dirs, files in os.walk(all_shits):
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
            return phoneme in ["pau", "AP", "SP"]

        phoneme_folder_path = all_shits
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
        phoneme_folder_path = all_shits
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
        print("writing vewels.txt...")
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

        for raw_folder_name in os.listdir(all_shits_not_wav_n_lab):
            raw_folder_path = os.path.join(all_shits_not_wav_n_lab, raw_folder_name)
            if any(filename.endswith(".lab") for filename in os.listdir(raw_folder_path)):
                print("segmenting data...")
                if estimate_midi.get() == "True":
                    subprocess.check_call(["python", "nnsvs-db-converter/db_converter.py", "-s", max_silence, "-S", max_silence_length, "-l", max_wav_length, "-m", "-c", "-L", "nnsvs-db-converter/lang.sample.json", "--folder", raw_folder_path])
                else:
                    subprocess.check_call(["python", "nnsvs-db-converter/db_converter.py", "-s", max_silence, "-S", max_silence_length, "-l", max_wav_length, "-L", "nnsvs-db-converter/lang.sample.json", "--folder", raw_folder_path])
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
    
    preprocess_button = tk.Button(right_frame, text = "Run Segmentation", font = ("Helvetica", 16), bg = bg, fg = fg, command = run_segment)
    preprocess_button.pack(pady=(20, 0))

    #===MAIN===#

    ########### MAX SILENCE AMOUNT
    def max_silence_slider(value):
        max_silence_interval.set(value)
        global max_silence
        max_silence = value
    max_silence_interval = tk.StringVar()
    max_silence_interval.set("2")
    max_silence_interval_label = tk.Label(window, text = "The maximum amount of silences (pau, SP, sil) in the middle of each segment", font = ("Helvetica", 12), bg = bg, fg = fg)  # Set fg to white
    max_silence_interval_label.pack(pady = (20, 0))
    max_silence_slider = tk.Scale(window, from_ = 0, to = 20, orient = "horizontal", resolution = 1, command = max_silence_slider, bg = bg, fg = fg)
    max_silence_slider.set(2)
    max_silence_slider.pack(pady = (10, 0))
    max_silence_label = tk.Label(window, textvariable = max_silence_interval, font = ("Helvetica", 12), bg = "#4B4B4B", fg = fg)
    max_silence_label.pack(pady = (10, 0))
    ###########

    ########### MAX SILENCE LENGTH
    def max_sil_length_slider(value):
        max_sil_length_interval.set(value)
        global max_silence_length
        max_silence_length = value
    max_sil_length_interval = tk.StringVar()
    max_sil_length_interval.set("0.5")
    max_sil_length_interval_label = tk.Label(window, text = "The maximum length for silences, convert to AP if exceed this value", font = ("Helvetica", 12), bg = bg, fg = fg)  # Set fg to white
    max_sil_length_interval_label.pack(pady = (20, 0))
    max_sil_length_slider = tk.Scale(window, from_ = 0, to = 45, orient = "horizontal", resolution = 0.5, command = max_sil_length_slider, bg = bg, fg = fg)
    max_sil_length_slider.set(0.5)
    max_sil_length_slider.pack(pady = (10, 0))
    max_sil_length_label = tk.Label(window, textvariable = max_sil_length_interval, font = ("Helvetica", 12), bg = "#4B4B4B", fg = fg)
    max_sil_length_label.pack(pady = (10, 0))
    ###########

    ########### MAX AUDIO LENGTH
    def max_wav_length_slider(value):
        max_wav_length_interval.set(value)
        global max_wav_length
        max_wav_length = value
    max_wav_length_interval = tk.StringVar()
    max_wav_length_interval.set("15")
    max_wav_length_interval_label = tk.Label(window, text = "The maximum length for audio segmentation", font = ("Helvetica", 12), bg = bg, fg = fg)  # Set fg to white
    max_wav_length_interval_label.pack(pady = (20, 0))
    max_wav_length_slider = tk.Scale(window, from_ = 0, to = 45, orient = "horizontal", resolution = 1, command = max_wav_length_slider, bg = bg, fg = fg)
    max_wav_length_slider.set(15)
    max_wav_length_slider.pack(pady = (10, 0))
    max_wav_length_label = tk.Label(window, textvariable = max_wav_length_interval, font = ("Helvetica", 12), bg = "#4B4B4B", fg = fg)
    max_wav_length_label.pack(pady = (10, 0))
    ###########

    ########### ESIMATE MIDI
    estimate_midi = tk.StringVar()
    estimate_midi.set("True")
    frame = tk.Frame(window, bg=bg)
    frame.pack(pady=(20, 10), padx=(20, 0), anchor="w")
    estimate_midi_option_label = tk.Label(frame, text="Estimate MIDI:", font=("Helvetica", 12), bg=bg, fg=fg)
    estimate_midi_option_label.pack(side="left", padx=(20, 0))
    estimate_midi_options = ["True", "False"]
    estimate_midi_drop_down = tk.OptionMenu(frame, estimate_midi, *estimate_midi_options)
    estimate_midi_drop_down.config(bg=bg, fg=fg, font=("Helvetica", 12))
    estimate_midi_drop_down.pack(side="right", padx=(20, 0))
    ###########

    ########### sussy
    sussy = tk.StringVar()
    sussy.set("Crewmate")
    frame = tk.Frame(window, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    sussy_option_label = tk.Label(frame, text ="Among Us:", font = ("Helvetica", 12), bg = bg, fg = fg)
    sussy_option_label.pack(side = "left", padx =(20, 0))
    sussy_options = ["Crewmate", "Imposter", "No Sussy Please"]
    sussy_drop_down = tk.OptionMenu(frame, sussy, *sussy_options)
    sussy_drop_down.config(bg = bg, fg = fg, font = ("Helvetica", 12))
    sussy_drop_down.pack(side = "right", padx = (20, 0))
    ###########


def config_screen():
    clear_screen(window)
    os.chdir(main_path)
    main_screen_txt.pack_forget()
    rawr_txt.pack_forget()

    relative_p = "            relative_path = filepath.relative_to(Path('.').resolve())"
    relative_change = f"            relative_path = filepath.relative_to(Path(r'{main_path}').resolve())"
    with open("DiffSinger/utils/training_utils.py", "r") as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if relative_p in line:
            lines[i] = relative_change + "\n"
            break
    with open("DiffSinger/utils/training_utils.py", "w") as file:
            file.writelines(lines)
    relative_p_2 = "        relative_path = filepath.relative_to(Path('.').resolve())"
    relative_change_2 = f"        relative_path = filepath.relative_to(Path(r'{main_path}').resolve())"
    with open("DiffSinger/utils/training_utils.py", "r") as file:
        lines_2 = file.readlines()
    for i, line in enumerate(lines):
        if relative_p_2 in line:
            lines_2[i] = relative_change_2 + "\n"
            break
    with open("DiffSinger/utils/training_utils.py", "w") as file:
            file.writelines(lines_2)

    #===SIDE===#
    right_frame = tk.Frame(window, bg = "#4B4B4B", width = 250)
    right_frame.pack(side = "right", fill = "both", expand = False)
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                                         ", fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    ########### ENERGY
    energy_training = tk.StringVar()
    energy_training.set("Train Energy: True")
    frame = tk.Frame(right_frame, bg = "#4B4B4B")
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    energy_training_options = ["Train Energy: True", "Train Energy: False"]
    energy_training_drop_down = tk.OptionMenu(frame, energy_training, *energy_training_options)
    energy_training_drop_down.config(bg = "#4B4B4B", fg = fg, font = ("Helvetica", 12))
    energy_training_drop_down.pack(side = "top", padx = (0, 0))
    ###########
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                                         ", fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    ########### BREATHINESS
    breathiness_training = tk.StringVar()
    breathiness_training.set("Train Breathiness: True")
    frame = tk.Frame(right_frame, bg = "#4B4B4B")
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    breathiness_training_options = ["Train Breathiness: True", "Train Breathiness: False"]
    breathiness_training_drop_down = tk.OptionMenu(frame, breathiness_training, *breathiness_training_options)
    breathiness_training_drop_down.config(bg = "#4B4B4B", fg = fg, font = ("Helvetica", 12))
    breathiness_training_drop_down.pack(side = "top", padx = (0, 0))
    ###########
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                                         ", fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    ########### PITCH
    pitch_training = tk.StringVar()
    pitch_training.set("Train Pitch: True")
    frame = tk.Frame(right_frame, bg = "#4B4B4B")
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    pitch_training_options = ["Train Pitch: True", "Train Pitch: False"]
    pitch_training_drop_down = tk.OptionMenu(frame, pitch_training, *pitch_training_options)
    pitch_training_drop_down.config(bg = "#4B4B4B", fg = fg, font = ("Helvetica", 12))
    pitch_training_drop_down.pack(side = "top", padx = (0, 0))
    ###########
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                                         ", fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr
    ########### DURATION
    duration_training = tk.StringVar()
    duration_training.set("Train Duration: True")
    frame = tk.Frame(right_frame, bg = "#4B4B4B")
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    duration_training_options = ["Train Duration: True", "Train Duration: False"]
    duration_training_drop_down = tk.OptionMenu(frame, duration_training, *duration_training_options)
    duration_training_drop_down.config(bg = "#4B4B4B", fg = fg, font = ("Helvetica", 12))
    duration_training_drop_down.pack(side = "top", padx = (0, 0))
    ###########
    #rawr
    frame = tk.Frame(right_frame, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "                                                         ", fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    #rawr

    #===MAIN===#

    ########## CONFIG TYPE SELECTION
    def set_config_type(value):
        global config_type
        config_type.set(value)
    config_type = tk.StringVar()
    config_type.set("Acoustic Training")
    config_type_list = ["Acoustic Training", "Variance Training"]
    config_type_drop_down = tk.OptionMenu(window, config_type, *config_type_list, command = set_config_type)
    config_type_drop_down.config(bg = bg, fg = fg, font = ("Helvetica", 12))
    config_type_drop_down.pack(pady=(20, 10))
    ###########

    ########### SHALLOW DIFF TRAINING SELECTION
    def enable_use_shallow_diffusion(value):
        global use_shallow_diffusion
        use_shallow_diffusion.set(value)
    use_shallow_diffusion = tk.StringVar()
    use_shallow_diffusion.set("True | gt_val")
    frame = tk.Frame(window, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    shallow_option_label = tk.Label(frame, text ="Use Shallow Diffusion:", font = ("Helvetica", 12), bg = bg, fg = fg)
    shallow_option_label.pack(side = "left", padx =(20, 0))
    shallow_options = ["True | gt_val", "True | aux_val", "False"]
    shallow_drop_down = tk.OptionMenu(frame, use_shallow_diffusion, *shallow_options, command=enable_use_shallow_diffusion)
    shallow_drop_down.config(bg = bg, fg = fg, font = ("Helvetica", 12))
    shallow_drop_down.pack(side = "right", padx = (20, 0))
    ###########

    ########### PRECISION OPTION
    def update_precision(selected_value):
        with open("DiffSinger/configs/base.yaml", "r") as config:
            config_data = yaml.safe_load(config)
        config_data["pl_trainer_precision"] = precision.get()
        with open("DiffSinger/configs/base.yaml", "w") as config:
            yaml.dump(config_data, config)
    precision = tk.StringVar()
    precision.set("32-true")
    frame = tk.Frame(window, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    precision_option_label = tk.Label(frame, text = "Training Precision:", font = ("Helvetica", 12), bg = bg, fg = fg)
    precision_option_label.pack(side = "left", padx =(20, 0))
    precision_options = ["32-true", "bf16-mixed", "16-mixed", "bf16", "16"]
    precision_drop_down = tk.OptionMenu(frame, precision, *precision_options, command = update_precision)
    precision_drop_down.config(bg = bg, fg = fg, font = ("Helvetica", 12))
    precision_drop_down.pack(side = "right", padx = (20, 0))
    ###########

    ########### BINARY SAVE DIR
    def binary_folder_save():
        global binary_save_dir
        binary_save_dir.set(filedialog.askdirectory())
    binary_save_dir.set("No folder selected")
    frame = tk.Frame(window, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    binary_save_label = tk.Label(frame, text = "Binary save folder:", font = ("Helvetica", 12), fg = fg, bg = bg)
    binary_save_label.pack(side = "left", padx = (20, 0))
    binary_save_button = tk.Button(frame, text = "Select Folder", font = ("Helvetica", 12), fg = fg, bg = bg, command = binary_folder_save)
    binary_save_button.pack(side = "right")
    binary_save_folder_label = tk.Label(window, textvariable = binary_save_dir, font = ("Helvetica", 12), fg = fg, bg = "#4B4B4B")
    binary_save_folder_label.pack(pady = (10, 0), padx = (40, 0), anchor = "w")
    ###########

    ########### MODEL SAVE DIR
    def model_folder_save():
        #global save_dir
        selected_folder = filedialog.askdirectory()
        if not selected_folder:
            return
        model_save_dir.set(selected_folder)
        save_dir = selected_folder
        search_text = "        args_work_dir = os.path.join("
        replacement = f"        args_work_dir = '{save_dir}'"
        with open("DiffSinger/utils/hparams.py", "r") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if search_text in line:
                lines[i] = replacement + "\n"
                break
        with open("DiffSinger/utils/hparams.py", "w") as file:
                file.writelines(lines)
        #incase if anyone wanna change it lmao
        search_text_alt = "        args_work_dir = '"
        replacement_alt = f"        args_work_dir = '{save_dir}'"
        with open("DiffSinger/utils/hparams.py", "r") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if search_text_alt in line:
                lines[i] = replacement_alt + "\n"
                break
        with open("DiffSinger/utils/hparams.py", "w") as file:
                file.writelines(lines)
    model_save_dir = tk.StringVar()
    model_save_dir.set("No folder selected")
    frame = tk.Frame(window, bg = bg)
    frame.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    model_save_label = tk.Label(frame, text = "Model save folder:", font = ("Helvetica", 12), fg = fg, bg = bg)
    model_save_label.pack(side = "left", padx = (20, 0))
    model_save_button = tk.Button(frame, text = "Select Folder", font = ("Helvetica", 12), fg = fg, bg = bg, command = model_folder_save)
    model_save_button.pack(side = "right")
    model_save_folder_label = tk.Label(window, textvariable = model_save_dir, font = ("Helvetica", 12), fg = fg, bg = "#4B4B4B")
    model_save_folder_label.pack(pady = (10, 0), padx = (40, 0), anchor = "w")
    ###########

    ########### DATA AUG SELECTION OPTION
    def set_data_aug(value):
        global data_aug
        data_aug.set(value)
    data_aug = tk.StringVar()
    data_aug.set("False")
    frame4 = tk.Frame(window, bg = bg)
    frame4.pack(pady = (20, 10), padx = (20, 0), anchor = "w")
    data_aug_option_label = tk.Label(frame4, text = "Use Data Augmentation:", font = ("Helvetica", 12), bg = bg, fg = fg)
    data_aug_option_label.pack(side = "left", padx = (20, 0))
    data_aug_options = ["True", "False"]
    data_aug_drop_down = tk.OptionMenu(frame4, data_aug, *data_aug_options, command = set_data_aug)
    data_aug_drop_down.config(bg = bg, fg = fg, font = ("Helvetica", 12))
    data_aug_drop_down.pack(side = "right", padx = (20, 0))
    ###########

    ########### SAVE STEP
    def set_save_interval(value):
        save_interval_v.set(value)
        global save_interval
        save_interval = value
    save_interval_v = tk.StringVar()
    save_interval_v.set("2000")
    save_interval_label = tk.Label(window, text = "Save Interval", font = ("Helvetica", 12), bg = bg, fg = fg)  # Set fg to white
    save_interval_label.pack(pady = (20, 0))
    set_save_interval = tk.Scale(window, from_ = 100, to = 10000, orient = "horizontal", resolution = 100, command = set_save_interval, bg = bg, fg = fg)
    set_save_interval.set(2000)
    set_save_interval.pack(pady = (10, 0))
    save_interval_value_label = tk.Label(window, textvariable = save_interval_v, font = ("Helvetica", 12), bg = "#4B4B4B", fg = fg)
    save_interval_value_label.pack(pady = (10, 0))
    ###########

    def run_preprocess():
        print("preprocessing...")
        spk_name = [folder_name for folder_name in os.listdir(all_shits_not_wav_n_lab) if os.path.isdir(os.path.join(all_shits_not_wav_n_lab, folder_name))]
        # i used spk_name for something else cus i forgor now imma just copy and paste it
        spk_names = [folder_name for folder_name in os.listdir(all_shits_not_wav_n_lab) if os.path.isdir(os.path.join(all_shits_not_wav_n_lab, folder_name))]
        num_spk = len(spk_name)
        raw_dir = []
        for folder_name in spk_name:
            raw_main = os.path.join(main_path, all_shits_not_wav_n_lab)
            folder_path = os.path.join(raw_main, folder_name)
            raw_dir.append(folder_path)
        if num_spk == 1:
            singer_type = "SINGLE-SPEAKER"
            diff_loss_type = "l2"
            f0_emb = "continuous"
            use_spk_id = False
            all_wav_files = []
            for root, dirs, files in os.walk("raw_data/diffsinger_db"):
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

        def update_yaml_config():
            enable_data_aug = data_aug.get()
            if enable_data_aug == "True":
                data_aug_enable = True
            else:
                data_aug_enable = False
            shallow = use_shallow_diffusion.get()
            if shallow == "True | gt_val":
                shallow_enable = True
                shallow_gt = True
            elif shallow == "True | aux_val":
                shallow_enable = True
                shallow_gt = False
            else:
                shallow_enable = False
                shallow_gt = False
            energy = energy_training.get()
            if energy == "Train Energy: True":
                energy_enable = True
            else:
                energy_enable = False
            brethiness = breathiness_training.get()
            if brethiness == "Train Breathiness: True":
                breathiness_enable = True
            else:
                breathiness_enable = False
            pitch = pitch_training.get()
            if pitch == "Train Pitch: True":
                pitch_enable = True
            else:
                pitch_enable = False
            duration = duration_training.get()
            if duration == "Train Duration: True":
                duration_enable = True
            else:
                duration_enable = False
            selected_config_type = config_type.get()
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
                bitch_ass_config["binary_data_dir"] = binary_save_dir.get()
                bitch_ass_config["dictionary"] = "dictionaries/custom_dict.txt"
                bitch_ass_config["augmentation_args"]["random_pitch_shifting"]["enabled"] = data_aug_enable
                bitch_ass_config["augmentation_args"]["random_time_stretching"]["enabled"] = data_aug_enable
                bitch_ass_config["use_key_shift_embed"] = data_aug_enable
                bitch_ass_config["use_speed_embed"] = data_aug_enable
                bitch_ass_config["max_batch_size"] = 9 #ive never tried reaching the limit so ill trust kei's setting for this
                bitch_ass_config["val_check_interval"] = int(save_interval)
                bitch_ass_config["use_energy_embed"] = energy_enable
                bitch_ass_config["use_breathiness_embed"] = breathiness_enable
                #shallow diff stuff
                bitch_ass_config["use_shallow_diffusion"] = shallow_enable
                bitch_ass_config["shallow_diffusion_args"]["val_gt_start"] = shallow_gt
                with open("DiffSinger/configs/acoustic.yaml", "w") as config:
                    yaml.dump(bitch_ass_config, config)

                # idk i just feel like 800 is a lil low for some people part 2
                new_f0_max = 1600
                og_script = "DiffSinger/utils/binarizer_utils.py"
                with open(og_script, 'r') as file:
                    mate = file.read()
                up_f0_val = mate.replace("f0_max = 800", f"f0_max = {new_f0_max}")
                with open(og_script, 'w') as file:
                    file.write(up_f0_val)

                os.chdir("DiffSinger")
                os.environ["PYTHONPATH"] = "."
                os.environ["CUDA_VISIBLE_DEVICES"] = "0"
                subprocess.check_call(["python", "scripts/binarize.py", "--config", "configs/acoustic.yaml"])


            else:
                with open("DiffSinger/configs/variance.yaml", "r") as config:
                    bitch_ass_config = yaml.safe_load(config)
                bitch_ass_config["speakers"] = spk_names
                bitch_ass_config["test_prefixes"] = random_ass_test_files
                bitch_ass_config["raw_data_dir"] = raw_dir
                bitch_ass_config["num_spk"] = num_spk
                bitch_ass_config["use_spk_id"] = use_spk_id
                bitch_ass_config["diff_loss_type"] = diff_loss_type
                bitch_ass_config["binary_data_dir"] = binary_save_dir.get()
                bitch_ass_config["dictionary"] = "dictionaries/custom_dict.txt"
                bitch_ass_config["max_batch_size"] = 9 #ive never tried reaching the limit so ill trust kei's setting for this
                bitch_ass_config["val_check_interval"] = int(save_interval)
                bitch_ass_config["predict_energy"] = energy_enable
                bitch_ass_config["predict_breathiness"] = breathiness_enable
                bitch_ass_config["predict_pitch"] = pitch_enable
                bitch_ass_config["predict_dur"] = duration_enable
                with open("DiffSinger/configs/variance.yaml", "w") as config:
                    yaml.dump(bitch_ass_config, config)

                # idk i just feel like 800 is a lil low for some people part 2
                new_f0_max = 1600
                og_script = "DiffSinger/utils/binarizer_utils.py"
                with open(og_script, 'r') as file:
                    mate = file.read()
                up_f0_val = mate.replace("f0_max = 800", f"f0_max = {new_f0_max}")
                with open(og_script, 'w') as file:
                    file.write(up_f0_val)

                os.chdir("DiffSinger")
                os.environ["PYTHONPATH"] = "."
                os.environ["CUDA_VISIBLE_DEVICES"] = "0"
                subprocess.check_call(["python", "DiffSinger/scripts/binarize.py", "--config", "DiffSinger/configs/variance.yaml"])

        update_yaml_config()
        os.chdir(main_path)

    preprocess_button = tk.Button(right_frame, text = "Run Preprocess", font = ("Helvetica", 18), bg = bg, fg = fg, command = run_preprocess)
    preprocess_button.pack(pady=(20, 0))

def training_screen():
    clear_screen(window)
    ########### SELECT CONFIG FILE
    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    def select_config_file():
        global config_file_path
        config_file_path.set(filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml")]))
    config_file_path.set("No file selected")
    config_file_label = tk.Label(window, text="Select Config File:", font=("Helvetica", 12), fg=fg, bg=bg)
    config_file_label.pack(side="top", pady=(0, 10))
    config_file_button = tk.Button(window, text="Browse", font=("Helvetica", 12), fg=fg, bg=bg, command=select_config_file)
    config_file_button.pack(side="top")
    config_file_path_label = tk.Label(window, textvariable=config_file_path, font=("Helvetica", 12), fg=fg, bg="#4B4B4B")
    config_file_path_label.pack(pady=(10, 0))
    ###########
    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    def select_model_save_path():
        global model_save_path
        model_save_path.set(filedialog.askdirectory())  # This will open a directory selection dialog

    model_save_path.set("No directory selected")
    model_save_label = tk.Label(window, text="Select Model Save Path:", font=("Helvetica", 12), fg=fg, bg=bg)
    model_save_label.pack(side="top", pady=(0, 10))
    model_save_button = tk.Button(window, text="Browse", font=("Helvetica", 12), fg=fg, bg=bg,
                                  command=select_model_save_path)
    model_save_button.pack(side="top")
    model_save_path_label = tk.Label(window, textvariable=model_save_path, font=("Helvetica", 12), fg=fg, bg="#4B4B4B")
    model_save_path_label.pack(pady=(10, 0))
    ###########

    def run_training():
        os.chdir("DiffSinger")
        os.environ["PYTHONPATH"] = "."
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        training_config = config_file_path.get()
        model_save_dir = model_save_path.get()
        subprocess.check_call(["python", "scripts/train.py", "--config", training_config, "--exp_name", model_save_dir, "--reset"])

    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))
    model_save_label = tk.Label(window, text = "                                            ", font = ("Helvetica", 9), fg = fg, bg = bg) #blank space for looks idk
    model_save_label.pack(side = "top", padx = (20, 0))

    preprocess_button = tk.Button(window, text = "Run Training", font = ("Helvetica", 18), bg = bg, fg = fg, command = run_training)
    preprocess_button.pack(pady=(20, 0))

def build_ou_vb():
    clear_screen(window)
    # text screen so it's not too empty
    wip_screen_txt = tk.Label(window, text = "Place Holder <3", font = ("Helvetica", 50), bg = bg, fg = fg)
    wip_screen_txt.pack(side = "top", pady = (225, 0))  # Add top padding
    rawr_txt = tk.Label(window, text = "will be here in later update i guess", font = ("Helvetica", 10), bg = bg, fg = fg)
    rawr_txt.pack(side = "top", pady = (20, 0))
    pass

def file_exit():
    window.quit()  # Close the application

file_menu = Menu(menubar, tearoff = 0)  # tearoff=0 prevents a dashed line from appearing at the top of the menu
menubar.add_cascade(label = "Option", menu = file_menu)
file_menu.add_command(label = "Download Dependencies", command = dl_scripts_github)
file_menu.add_separator()
file_menu.add_command(label = "Segment & Process Data", command = segment_screen)
file_menu.add_command(label = "Edit Config & Preprocess", command = config_screen)
file_menu.add_command(label = "Train Model", command = training_screen)
file_menu.add_command(label = "Build OpenUtau Voicebank", command = build_ou_vb)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command = file_exit)

window.mainloop()
