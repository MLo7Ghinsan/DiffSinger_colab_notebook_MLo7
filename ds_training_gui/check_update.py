import requests
import re
from tkinter import messagebox


gui_github = requests.get("https://raw.githubusercontent.com/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/main/ds_training_gui/ds_gui.py")
github_version = re.search(r'version\s*=\s*[\'"]([^\'"]+)[\'"]', gui_github.text)
github_version = github_version.group(1)

with open("ds_gui.py", "r", encoding = "utf-8") as gui_local:
	gui_local = gui_local.read()
local_version = re.search(r'version\s*=\s*[\'"]([^\'"]+)[\'"]', gui_local)
local_version = local_version.group(1)

if local_version == github_version:
	pass
else:
	update_prompt = messagebox.askyesno("Notice", f"Latest ds_gui version is {github_version}.\n\nYou currently have {local_version}.\n\nWould you like to update ds_gui?")
	if update_prompt:
		with open("ds_gui.py", "wb") as gui_script:
			gui_script.write(gui_github.content)
	else:
		pass

from ds_gui import App #import later to prevent the app from using the older ver <3
if __name__ == "__main__":
	app = App()
	app.mainloop()
