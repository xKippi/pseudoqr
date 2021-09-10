# pseudoqr
This is a simple Python script to generate pseudo QR Codes. These fake QR Codes look and feel just like regular ones but are unscanable and useless. In fact, they are just a random arrangement of black dots with the visually most prominent key elements of a QR Code, namely the position ("edge") and alignment ("middle point") structures.

## Usage
To use this you have to set the QR Code version (for details see [below](#qr-code-version)) and the output file either as parameters or via command line arguments. You can also adjust the other variables to your behalf.

### Command Line Arguments
To learn more about the available command line arguments, run `pseudoqr.py -h`
    
### Parameters
The adjustable parameters are located in the section denoted with `--- BEGIN CONFIG ---`. To learn more about those parameters just have a look at the comments above them.

## Bugs
If you find a bug you can keep it! Just kidding, please create an issue in this repository.

# QR Code Version
The QR Code version is basically just a paraphrase for the size of a QR Code. For example, a version 1 QR Code is 21 x 21 modules (a module is just a black dot). For more information and a list describing the size and data storage capabilities of different QR Code version see [https://www.qrcode.com/en/about/version.html](https://www.qrcode.com/en/about/version.html).

# Disclaimer
The script here is only provided for educational purposes. I am not responsible for anything **you** decide to do with this script.