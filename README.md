# DEN Video Downloader

Download USC DEN lecture videos beyond limitations. 
You can download one video or all videos of a specific course from DEN.

* `.ts` file format with H.264 and AAC coded.
* No expiration dates.
* No DEN Player needed.
* No anything but the lecture videos.

### Pre-requisites

* Windows
* macOS/Linux (tested OK on macOS 10.11/10.12 and Ubuntu 14.04)
* Python 3 (Install on [macOS](https://docs.python.org/3/using/mac.html)/[Ubuntu](http://askubuntu.com/questions/682869/how-do-i-install-newer-python-versions-using-apt-get))
* selenium is required to run dendown_all.py. run 'pip install selenium' or use anaconda to install selenium.
* a chromedriver executable is required for selenium. download chromdriver from https://chromedriver.storage.googleapis.com/index.html?path=2.38/ and set up the 'PATH' variable in the environment where the downloading script is running or put the chromedriver exectable under a 'PATH' directory.

### Usage

#### Download One Video

* Log into USC DEN.
* Open any lecture video.
* Copy the link of `Android / iOS` button.
![copy-link](./copy-link.png)
* Open terminal and `cd` into the directory contains the script.
* Run with command:
    ```
    python3 ./dendown.py [url_copied_from_the_webpage]
    ```
* Wait the download process to complete.

#### Download All Videos of a Specific Course

* Open terminal and `cd` into the directory contains the script.
* Make sure you have selenium installed and chromedriver exectable under your 'PATH'
* Run with command:
	```
	python3 ./dendown_all.py [Username] [Password] [Course]
	```
* Course is a string that represents the course to download. E.g.: CSCI567

* Wait the download process to complete.

### Acknowledgements

This script is only for convenience of downloading lecture videos only. The author is not responsible for the use and its subsequence.

License: [MIT License](./LICENSE)
