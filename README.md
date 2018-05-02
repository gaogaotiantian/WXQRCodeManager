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

### Activate Virtual Environment
```
python -m venv QRCodeReader.QRCodeVal
source QRCodeReader.QRCodeVal/bin/activate
```
To deactivate it, just run
```
deactivate
```

### Run Gunicorn
```
gunicorn app:app
```
