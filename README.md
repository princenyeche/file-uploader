# Image Uploader
An Image Micro Service - This Service is used to Store Images for single files and multiple files and output the direct url link.Basically it doesn't have to be an Image, you can change to any file you want but the example on this Repo is using an Image.

### Use Case
* You can use this script as an example to understand how images / file can be uploaded to a Server by an Anonymous user
* You can use this as an example in your Project.


### Configurations

* Clone the Repo into your local machine.
* ensure you have Python Installed or Goto https://www.python.org/downloads/ any version from v3.6.x will do.
* if you're not on python3.6, you can use a virtual environment to run the App `python -m virtualenv venv --python=3.6`.
* Then activate it by using `source venv/bin/activate`
* You will also need to ensure you have PIP on your computer with the download. check by using `pip --version`
* You will need to install Flask module, do so by using `pip install -r requirements.txt`
* Once installed, `cd` into the directory so you can run a local server on Terminal by doing the below
```bash
$: export FLASK_APP=uploader && FLASK_ENV=development 
$: flask run
```
* This will start up a local server with debug mode on. If you do not want debug on, you can set `FLASK_ENV=production`
* Access the Service by navigating to your browser on http://127.0.0.1:5000

### Accessing via GUI 

* This Service comes with a UI base, where you can access the Service
* Navigate on your Browser on http://127.0.0.1:5000 to begin

### Accessing via REST 

* This Service also has a REST method as well, were you can send request via HTTP
* endpoint for the resource is http://127.0.0.1:5000/api
* Using cURL as an example cd into the directory where an image file is located
    ```bash
    curl -X POST -F "file=@file.png" "http://127.0.0.1:5000/api"
    ```
  *OR*
    ```bash
    curl -X POST -F "file=@Archive.zip" "http://127.0.0.1:5000/api"
    ```
#### Output for multiple file upload
   ```bash
   {
  "results": [
    {
      "message": "File has been uploaded link http://127.0.0.1:5000/view/script_field1.png", 
      "status": "success"
    }, 
    {
      "message": "File has been uploaded link http://127.0.0.1:5000/view/updatesql.png", 
      "status": "success"
    }
  ]
  }
   ```

### Improvements ###

* The URL cannot be viewed later on for multi upload after the current browser tab has been close.
* The directory search is only one layer, cannot search files within another layer of folder.
* Files are overwritten, if they bear the same name.
