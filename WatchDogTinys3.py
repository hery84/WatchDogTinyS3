#!/usr/bin/python
import sys, time, logging, tinys3, shutil, os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class OnCreatedHandler(PatternMatchingEventHandler):
    patterns = ["*.jpg", "*.png"] # FileType ("*.mp4","*.txt", etc..)
    def on_created(self, event):
        S3_ACCESS_KEY="<YOURS3ACCESSKEY>"
        S3_SECRET_KEY="<YOURS3SECRETSKEY>"
        S3_BUCKET="website" 
        S3_DIRECTORY="/images" #S3 Directory inside S3_BUCKET (.../website/images)
        PATH_DST="/Users/username/tmp" # Optional: Directory 
        conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY)       
        logging.info('Uploading File: %s',event.src_path)
        f = open(event.src_path,'rb')
        r = conn.upload(os.path.basename(event.src_path),f,S3_BUCKET+S3_DIRECTORY)
        if r.status_code == 200:
            logging.info('Uploaded: %s',os.path.basename(event.src_path))
            shutil.move(event.src_path, PATH_DST) #Optional: On upload success Move the file to PATH_DST
        else:
            logging.info('Error: %s',r)
        f.close()

if __name__ == "__main__":
    LOG_FILENAME = 'out.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,
        format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    observer.schedule(OnCreatedHandler(), path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
