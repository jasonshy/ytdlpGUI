from tkinter import *
import customtkinter
import yt_dlp
import os
from tkinter import filedialog

#Create the main window
app = customtkinter.CTk()
app.geometry("1800x360")
app.title("Downloader")
customtkinter.set_appearance_mode("system")
app.resizable(False, False)
#Font
my_font = customtkinter.CTkFont(family = "Arial", size = 12)




########################################################################### Read the setting file for the previous path and file type #######################################################################
def readFile():
    	try:
        	with open("dl_settings.txt", "r") as file:
        		return file.read().split('\n') # Read and strip any extra whitespace
    	except FileNotFoundError:
        	return "Select Save Path"  # Default value if the file doesn't exist
settings = readFile()
fileType = settings[0]
path = settings[1]
print(fileType, path, "To show the previous settings.")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




########################################################################################## UpperFrame #######################################################################################################
upperFrame = customtkinter.CTkFrame(master = app,
				     width = 1780,
				     height = 150, 
				     border_width = 1, 
				     border_color = "#ff5b00", 
				     corner_radius = 0, 
				     fg_color = "black")

upperFrame.pack(pady = 10)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




########################################################################################## URL Entry ########################################################################################################
entry = customtkinter.CTkEntry(master = upperFrame,
                               placeholder_text = "Paste the URL here.", 
                               justify = "center", 
                               width = 1500, 
                               corner_radius = 0,
                               font = (my_font))
                               
entry.place(relx = 0.5, rely = 0.5, anchor = "center")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




#Option Frame
optionFrame = customtkinter.CTkFrame(master = app, 
			              width = 380, 
			              height = 190, 
			              border_width = 1, 
			              border_color = "#ff5b00",
			              corner_radius = 0, 
			              fg_color = "black")
			              
optionFrame.pack(side = "left", padx = 10)

#Mp3/4 Option menu

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Change file type
def writeFileType(choice):
	try:
		with open("dl_settings.txt", "r") as file:
			newSettings = file.read().split("\n")
		newSettings[0] = choice + "\n"
		with open('dl_settings.txt', 'w') as file:
    			file.writelines(newSettings)
		print(newSettings)
	except Exception as e:
		print(f"Error occurred: {e}")
		

combobox = customtkinter.CTkOptionMenu(master = optionFrame,
                                       values = ["MP3", "MP4"],
                                       command = writeFileType,
                                       width = 320,
                                       fg_color="black",
                                       button_color="#ff5b00",
                                       font = (my_font))
                                       
combobox.place(relx = 0.5, rely = 0.5, anchor = "center")
combobox.set(fileType)  # set initial value




###################################################################################Path Frame##################################################################################################################
#Path Frame
pathFrame = customtkinter.CTkFrame(master = app,
                                   width = 1000, 
                                   height = 190, 
                                   border_width = 1, 
                                   border_color = "#ff5b00", 
                                   corner_radius = 0, 
                                   fg_color = "black")
                                   
pathFrame.pack(side = "left")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




#Path Selecting Button
def select_path():
	# Open a file dialog to select the path where the file will be saved
	directory_path = filedialog.askdirectory()  # This will allow users to select a directory
	select_path_button.configure(text=directory_path)
	with open("dl_settings.txt", "r") as file:
		settings = file.read().split("\n")
	newSettings = [(settings[0] + "\n"), directory_path]
	with open('dl_settings.txt', 'w') as file:
    		file.writelines(newSettings)
	return directory_path


select_path_button = customtkinter.CTkButton(master = pathFrame, text = path ,command = select_path, width = 750, border_color="#ff5b00",  
                                             border_width=1,
                                             corner_radius = 0,
                                             fg_color = "black",
                                             font = (my_font))
                                             
select_path_button.place(relx = 0.5, rely = 0.5, anchor = "center")


######################## Download button frame
dlFrame = customtkinter.CTkFrame(master = app, width = 380, height = 190, border_width = 1, border_color = "#ff5b00", corner_radius = 0, fg_color = "black")
dlFrame.pack(side = "left", padx = 10)


######################## Download button
def press_to_download():
	url = entry.get()
	if not url:
		print("the fuck?")
		return
	with open("dl_settings.txt", "r") as file:
		settings = file.read().split('\n')
		fileType = settings[0]
		savePath = settings[1]
	if not os.path.isdir(savePath):
		print("the fuck?")
		return
	# Set yt-dlp options
	ydl_opts = {}
	if fileType == "MP3":
		ydl_opts = {"format": "bestaudio/best", 
		            "outtmpl": os.path.join(savePath, "%(title)s.%(ext)s"),
		            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320',
		            }],}
	elif fileType == "MP4":
		ydl_opts = {"format": "bestvideo+bestaudio",
		            "outtmpl": os.path.join(savePath,
		             "%(title)s.%(ext)s"),}
				
				
    # Download the video using yt-dlp
	try:
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
		print("Download completed successfully")
	except Exception as e:
		print(f"Error during download: {e}")
	
	
	
	
	
	
	
	
	
	
	


dl_button = customtkinter.CTkButton(master = dlFrame, text = "Download" ,command = press_to_download, width = 300, border_color="#ff5b00",  
                                             border_width=1,
                                             corner_radius = 0,
                                             fg_color = "black",
                                             font = (my_font))

dl_button.place(relx = 0.5, rely = 0.5, anchor = "center")


































app.mainloop()
