#author          :Alireza Tajadod in Dr.Jennifer Ryan's lab
#date            :02/05/18
#usage           :python3 pyscript.py
#documentation   :Audio_Transcriber.pdf
#python_version  :3.6 
#author-contact  :ATajadod@research.baycrest.org



## =================  IMPORT STATEMENTS  =================
print(' Initializig... ')

import os
import csv
import sys

try:
    from google.cloud import storage
    from google.cloud import speech

except ImportError:
    print('You need to install google.cloud.storage and google.cloud.speech in order to use this application')
    quit()

from google.cloud.speech import enums
from google.cloud.speech import types 


# Gui imports 
from tkinter import Tk
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
root.update()




## =================  GOOGLE CREDENTIAL =================
change_credential = messagebox.askyesno("Audio_Transcriber","Would you like to change the default Google Credential?")
if change_credential:
	filename = askopenfilename(title = 'Please Select your credential File') # show an "Open" dialog box and return the path to the selected file
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = filename
else: 
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../Credentials/ryan_1801_eye_movement.json'

try: 
	storage_client = storage.Client()
	print('Google account access: Success')
except:
	print(os.getcwd())
	print('Can not access Service account')

# ====  Setting up the bucket  ====
try: 
	bucket_name = 'ryan-1801-reb0201-eye-movement-bucket'
	bucket = storage_client.get_bucket(bucket_name)
	print('Bucket account access: Success')
except:
	print("Bukcet access error")

# ====  Setting up the speech recognizer  ====  
try: 
	speech_client = speech.SpeechClient()
	print('Speech account access: Success')
except:
	print ("Speech_recognition access error")


## =================  AUDIO SET UP  =================

uri = bucket_name + '/audio_data'
audio = types.RecognitionAudio(uri='gs://ryan-1801-reb0201-eye-movement-bucket/audio_data')
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=24000,
    language_code='en-US',	
    enable_word_time_offsets=True)
    #enable_automatic_punctuation= True)


 
## =================  INPUT FOLDERS  =================
title = 'Please select your input folder or cancel if finished'
Data_folders = []
while True:
	dir = filedialog.askdirectory(title=title)
	if not dir:	
		break
	Data_folders.append(dir)
	title = 'got %s. Next dir' % dir

root.update()


## =================  CREATING OUTPUTS  =================
for Data_folder in Data_folders:
	Output_folder = Data_folder + '/GTranscriber_output/'
	try:
		os.mkdir(Output_folder)
		os.mkdir(Output_folder + 'Full_information')
		os.mkdir(Output_folder + 'Timetable')
		os.mkdir(Output_folder + 'Transcript')
	except OSError as exception:
		if not os.path.isdir(Output_folder):
			raise

	print('Getting All files from: ' + Data_folder)
	print('Outputfile set to: ' + Output_folder)

	for file in os.listdir(Data_folder):

		filename_base = os.path.splitext(file)[0]
		filename_ext = os.path.splitext(file)[-1]

		if filename_ext in ['.wav', '.mp3']  :   # more audio extensions can be added here. eg:  if filename_ext in ['.wav', '.mp3', '.extension'] 
			trial = os.path.join(Data_folder , file)
			blob = bucket.blob('audio_data')
			blob.upload_from_filename(trial)
			operation = speech_client.long_running_recognize(config, audio)

			
			print('Now trying : ' + filename_base)
			print('Waiting for operation to complete...')
			try:
				result = operation.result(timeout = 300)
				print(filename_base + ': Succesful')

				with open(Output_folder + 'full_Information/' + filename_base + '_detailed_transcript.txt', 'w') as detailed_output_file:
					for myresult in result.results:
						alternative = myresult.alternatives[0]
						detailed_output_file.write('Transcript: {} \n'.format(alternative.transcript))
						detailed_output_file.write('Confidence: {} \n'.format(alternative.confidence))

						for word_info in alternative.words:
							word = word_info.word
							start_time = word_info.start_time
							end_time = word_info.end_time
							detailed_output_file.write('Word: {}, start_time: {}, end_time: {} \n'.format(
								word,
								start_time.seconds + start_time.nanos * 1e-9,
								end_time.seconds + end_time.nanos * 1e-9))


				print( 'Succesfully created: ' + detailed_output_file.name)

				with open(Output_folder + 'Transcript/' + filename_base + '_transcript.txt','w') as output_file:
					for myresult in result.results:
						alternative = myresult.alternatives[0]
						output_file.write(format(alternative.transcript))

				print( 'Succesfully created: ' + output_file.name)


				with open(Output_folder + 'Timetable/' + filename_base + '_timetable.csv', 'w') as csv_file:
					csvwriter = csv.writer(csv_file, dialect='excel')
					for myresult in result.results:
						alternative = myresult.alternatives[0]
						for word_info in alternative.words:
							word = word_info.word
							start_time = word_info.start_time.seconds + word_info.start_time.nanos * 1e-9
							end_time = word_info.end_time.seconds + word_info.end_time.nanos * 1e-9
							output = [word,start_time,end_time,end_time - start_time]
							csvwriter.writerow(output)
					print('Succesfully created: ' + csv_file.name)

			except:
				print(trial + 'skipped')
				continue

blob.delete()
sys.stdout = old_stdout
log_file.close()





'''
Written by Alireza Tajadod 
May 1/ 2018
'''	