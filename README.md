# Getting Started

## Installation

### Python Version
3.6

### Install Requirements
```
pip install -r /path/to/requirements.txt
```
If you are using MAC and you encountered problem related to zbar, try run
```
brew install zbar
```

### You need tesseract for running this
On Linux, use
```
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim
```

On Mac OS, use
```
brew install tesseract --with-all-languages
```

## Run Test for the Module

### Run local server
```
gunicorn app:app
```

### Run QRCodeReader Test
```
python -m QRCodeReader.QRCodeTest
```

### Run back-end test
```
cd test
python ServerVal.py <server_url>
```
example:
```
python ServerVal.py https://wxqrcodemanager.herokuapp.com
python ServerVal.py localhost:8000
```
