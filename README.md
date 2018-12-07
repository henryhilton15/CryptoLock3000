# CryptoLock3000
Cryptographic Password Manager
Tom Jones, David Lee, Henry Hilton

Implementation of basic command line version complete.

Run from terminal with `python master_password.py` and follow prompts.

To clear data and start fresh, simply open `infofile.txt` and delete the saved encrypted data.

We are working on a nice little GUI that runs our program as a stretch goal for the presentation, you can launch the GUI to see what it will be like with `python GUI.py`. Launching the GUI launches a simultaneous subprocess on a different thread that runs `master_password.py`. The rest of the communication between GUI and the command line program is in the works.
