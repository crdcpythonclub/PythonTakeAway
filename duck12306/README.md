
# Duck12306

*Original idea comes from https://github.com/andelf/fuck12306. This repo forks it for extension and BUG Fixing*

# Installation

1. Install pip

	```
	sudo apt-get install python-pip python-dev
	```

2. Install preresquites

	```
	sudo apt-get install python-imaging
	sudo apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms1-dev libwebp-dev
	```

3. Install Pillow

	```
	sudo pip install pillow
	```

4. Install leptonica from http://www.leptonica.com/download.html

	```
	wget http://www.leptonica.com/source/leptonica-1.71.tar.gz
	tar -xvf leptonica-1.71.tar.gz
	cd leptonica-1.71/
	sudo ./configure
	sudo make
	sudo make install
	```

5. Install tesseract from https://code.google.com/p/tesseract-ocr/

	```
	wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.02.tar.gz
	tar -xvf tesseract-ocr-3.02.02.tar.gz
	cd tesseract-ocr/
	sudo ./configure
	sudo make
	sudo make install
	sudo ldconfig
	```

6. Copy trained data (English, Chinese) to tesseract

	```
	cd ~
	wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.eng.tar.gz
	wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.chi_sim.tar.gz
	tar -xvf tesseract-ocr-3.02.eng.tar.gz
	tar -xvf tesseract-ocr-3.02.chi_sim.tar.gz
	sudo cp tesseract-ocr/tessdata/*.traineddata /usr/local/share/tessdata/
	```

7. Clone pytesseract and install

	```
	cd ~
	git clone https://github.com/crdcpythonclub/pytesseract.git
	cd pytesseract/
	sudo python setup.py install
	```

8. Clone duck12306 and run it

	```
	cd ~
	git clone https://github.com/crdcpythonclub/PythonTakeAway.git
	cd PythonTakeAway/duck12306
	python duck12306.py
	```

9. Now you go!

# Error handling


 - `IOError: decoder jpeg not available`


	Install preresquites above
	Re-install Pillow
	
	```
	sudo pip install -I pillow
	``` 


- `UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)`


	Change python default encoding to utf8
	
	```
	export PYTHONIOENCODING=utf8
	```


- `TesseractError: (127, 'tesseract: error while loading shared libraries: libtesseract.so.3: cannot open shared object file: No such file or directory')`


	see 'Install tesseract'


- `TesseractError: (1, 'Error opening data file /usr/local/share/tessdata/eng.traineddata')`


	see 'Copy trained data (English, Chinese) to tesseract'


# Additions

## Tesseract

Tesseract is an optical character recognition engine for various operating systems. It is free software, released under the Apache License, Version 2.0, and development has been sponsored by Google since 2006. Tesseract is considered one of the most accurate open source OCR engines currently available

Leptonica is a pedagogically-oriented open source site containing software that is broadly useful for image processing and image analysis applications.

## PIL and pillow

Python Imaging Library (abbreviated as PIL) is a free library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats. It is available for Windows, Mac OS X and Linux. 

Development appears to be discontinued with the last commit to the PIL repository coming in 2011. Consequently, a successor project called Pillow has forked the PIL repository and added Python 3.x support. This fork has been adopted as a replacement for the original PIL in Linux distributions.



