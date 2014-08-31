#PetBot listen

An open source repository for [PetBot](http://petbot.ca) bark recognition software.

Here we store code to recognize dog barks from a microphone on the raspberry pi.

Included in this repository is:

* **src/listen_for_bark.c** - The main executable, listens over ALSA and runs the LR model in realtime
* **src/run_model.c** - Load LR model and run on output from capture
* **src/capture.c** - Listen on microphone and collect data already passed through FFT
* **src/classify.py** - Train a LR (Logistic regression) model on output of capture
* **model/** - Contains trained LR models

## License
All content here is licensed under  GNU General Public License v3.0
