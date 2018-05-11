# Documentaiton for Audio_Transcriber.py

## First Time Use

```
Using the bash application:
```
Place Audio_Transcriber.command in your desired folder. Place the Audio_Transcriber.py file in
yourdesiredfolder/Scripts/Google_Transcription/Audio_Transcriber.py. Alternatively you can change
Audio_Transcriber.command by opening it as a text file and altering the directory as shown below.

In [ ]:

```
cd ./Scripts/Google_Transcribtion #can be changed: cd path/to/Audio_Transcriber
.py
```
If the environemnt has previously been configured, run the Audio_Transcriber.command application by
double clicking on it.

```
Using the python script:
```
Run the python script using your prefered method. Forexample, you can open terminal in the script's
directory and type : python3 Audio_Transcriber.py


## Requirments

### Required Google credentials

```
Google_Application_Credential You should have a json file with your google credentials
(https://cloud.google.com/docs/authentication/production/). The Json file should be produced
after google transcription services are purchased
Google_Bucket You should have a google bucket
(https://cloud.google.com/storage/docs/json_api/v1/buckets).
```
```
Please note that your google credentials must have the correct to use the bucket.
```
### Required Python Pacakges

```
os
csv
tkinter
google.cloud
```
The os,csv and tkinter package are included in the standard python download and should not require further
installation

The Google.cloud package can be found here (https://pypi.org/project/google-cloud/) or simply installed on
terminal via:

pip install google-cloud

## Undestanding/configuring Audio_Transcriber.py

Simply run the Audio_Transcriber script using python and follow the instructions. Use the bash to check on
the script's progress

### Credentials

The first pop up window will ask you for your google credentials file. If you choose not to provide a json file,
on trusted computer simply alter the else statement on the Google Credential section of the script as shown
below:


In [ ]:

```
## ================= GOOGLE CREDENTIAL =================
change_credential = messagebox.askyesno("Audio_Transcriber","Would you like to c
hange the default Google Credential?")
if change_credential:
filename = askopenfilename(title = 'Please Select your credential File')
# show an "Open" dialog box and return the path to the selected file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = filename
else :
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Path/to/your/file.json'
```
You will also need to change the bucket name under the "setting up the bucket" subsection shown below:

In [ ]:

```
# ==== Setting up the bucket ====
try :
bucket_name = 'ryan-1801-reb0201-eye-movement-bucket'
bucket = storage_client.get_bucket(bucket_name)
```
### Audio files

The default configuration for audio files is shown below. It can be altered in the Audio setup section of the
script. More information can be found here (https://cloud.google.com/speech-to-
text/docs/reference/rest/v1/RecognitionConfig)

In [ ]:

```
## ================= AUDIO SET UP =================
```
```
config = types.RecognitionConfig(
encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
sample_rate_hertz= 24000 ,
language_code='en-US',
enable_word_time_offsets= True )
```

### Input

The program will promt you asking for your input folder. Simply choose as many folders as you would like to
transcribe. Once finished, cancel the folder selecter. Your folders are saved as the Data_folders variable and
outputted on the terminal and saved after in the log file.

```
The program only recognizes .wav or .mp3 files as audio files. Find the line below in the program
and adjust it accordingly if needed.
```
In [ ]:

```
if filename_ext in ['.wav', '.mp3'] : # more audio extensions
can be added here. eg: if filename_ext in ['.wav', '.mp3', '.extension']
```
```
The program will transcribe every audio file in the selected folders. All non audio files will be
skipped. If no audio files exist in the selected folder, your output folder will be empty.
By default, the program creates a blob (http://google-cloud-
python.readthedocs.io/en/latest/storage/blobs.html) named audio_data to your bucket. It uploads
and transcribes each file sequentially, overwriting the older file. At the end, the blob is deleted and
none of files will remain on google storage.
```
### Output

An indepdent output folder is created for all selected input folders named GTranscriber_output. Three nested
subfolders are then created, each containing a file for every audio file. All output files are named the same as
the input file with respective subscript (subfolder name) explained below.

```
Transcript: This folder contains txt files for each audio file with Google's transcript.
Timetable: This folder contains excel optimized csv files with the start time, end time and duration
of each spoken word.
Full_information: This folder contains txt files with detailed information on the transcript. It incldues
the Confidence percentage assigned by google.
```
Output details can be found in the creating outputs section. Changing this section is not recomended unless
the user is familiar with the _os.path_ package and google's _long_running_recognize_ return object. The lines
copied below interact with google, everything else is done using the returned value.

In [ ]:

```
operation = speech_client.long_running_recognize(config, audio)
result = operation.result(timeout = 300 )
```

## Notes

```
As shown in the result line above, a 300 second transcription timeout it set. This should but may not
be enough for files as long as 30 minutes. If a transcription is timed out, the file is skipped.
Once started, the program can only be stopped by manually closing the terminal.
The terminal window opened by running the application contains all relevant information for the
applicaiton's progress. In case of failure please read the window closely to see what it did
succesfully and what it failed to do.
```

