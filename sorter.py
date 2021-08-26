from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog, messagebox
from fileHandler import *

def update_image_viewer(img_path):
    if img_path != None:
        img2 = ImageTk.PhotoImage(Image.open(img_path))
        image_viewer.configure(image=img2)
        image_viewer.image = img2

def onKeyPress(event):
    key_pressed = event.char
    global current_image_path
    fh.update(key_pressed)
    current_image_path = fh.current_file
    update_image_viewer(current_image_path)

def select_directory_working():
    selected_dir = filedialog.askdirectory()
    working_dir_var.set(selected_dir + "/")

def select_directory_output():
    selected_dir = filedialog.askdirectory()
    output_dir_var.set(selected_dir + '/')

def start():
    working_dir = working_dir_var.get()
    output_dir = output_dir_var.get()
    if len(working_dir) > 0 and len(output_dir) > 0:
        fh.reset(working_dir, output_dir)
        current_image_path = fh.current_file
        update_image_viewer(current_image_path)

if __name__ == '__main__':
	fh = FileHandler()

	root = Tk()
	root.geometry("800x600")
	root.title("Dataset Builder")

	notebook = ttk.Notebook(root)
	notebook.pack(expand = True)

	frame_sorting = ttk.Frame(notebook, width = 800, height = 600)
	frame_sorting.pack(fill=BOTH, expand=True)

	# Button to select working directory
	select_working_dir_btn = ttk.Button(frame_sorting, text = "select working directory", command = select_directory_working)
	select_working_dir_btn.place(x=100,y=10)

	# label to show working directory
	working_dir_var = StringVar()
	working_dir_var.set("")
	label_working_dir = ttk.Label(frame_sorting, textvariable = working_dir_var)
	label_working_dir.place(x=290,y=10)

	# Button to select directory where valid image will be moved to 
	select_output_dir_btn = ttk.Button(frame_sorting, text = "select output directory", command = select_directory_output)
	select_output_dir_btn.place(x = 100, y = 40)

	#label to show output directory
	output_dir_var = StringVar()
	output_dir_var.set("")
	label_output_dir = ttk.Label(frame_sorting, textvariable = output_dir_var)
	label_output_dir.place(x = 290, y = 40)

	# load images
	start_btn = ttk.Button(frame_sorting, text = "Start", command = start)
	start_btn.pack(pady = 70)
	# image Viewer
	current_image_path = 'blank.png'
	img = ImageTk.PhotoImage(Image.open(current_image_path))
	image_viewer = Label(frame_sorting, image=img)
	image_viewer.pack()

	# info label
	label_info = ttk.Label(frame_sorting, text = "press: 0 for invalid pictures\npress: 1 for valid pictures\npress: LEFT ARROW to backtrack")
	label_info.pack(side=BOTTOM)

	notebook.add(frame_sorting, text = "Data Sorting")

	# GUI for web scraping 
	frame_data_colection = ttk.Frame(notebook, width = 800, height = 600)
	frame_data_colection.pack(fill = 'both', expand = True)
	notebook.add(frame_data_colection, text = 'Web Scraping')

	root.bind('<KeyPress>', onKeyPress)
	root.mainloop()