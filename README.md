# <img width="24" height="24" alt="f__1_-removebg-preview" src="https://github.com/user-attachments/assets/3277efc1-34a5-4f88-9b9c-34e10660c0a7" /> Focus Button 


A simple focus timer program built using **Tkinter** and **CustomTkinter** which can be bundled as a macOS app using **PyInstaller**.
The user can choose a timer duration and optionally open preset links at the beginning of each focus session. 
An alarm sounds at the end of the session.



## 📋 Features
- Start, pause, resume, and reset the focus timer
- Add custom links that open automatically at the start of a session
- Custom timer durations
- Simple UI
- Can be bundled as a macOS app with custom icon

---

<img width="287" height="198" alt="Screenshot 2025-12-02 at 16 52 08" src="https://github.com/user-attachments/assets/36af4a50-b4dd-42a4-be89-49b4ef61f944" />
<img width="287" height="198" alt="Screenshot 2025-12-02 at 16 52 14" src="https://github.com/user-attachments/assets/0a17bd45-6baf-4d02-b4ab-74cbe0a244e5" />
<img width="235" height="391" alt="Screenshot 2025-12-02 at 16 52 25" src="https://github.com/user-attachments/assets/b91e217f-3615-4de3-8617-cf20824f5724" />




## 🧰 Requirements
```
customtkinter
```

## 🏁 Run the App
```
python3 main.py
```
## 🛠️ Build the macOS App
Inside the project folder: 

1) Create a virtual environment
```
python3 -m venv venv
```
2) Activate virtual environment
```
source venv/bin/activate
```
3) Install requirements
```bash
pip install -r requirements.txt
```
4) Install PyInstaller
```bash
pip install pyinstaller
```
5) Build the app using PyInstaller 
```bash
pyinstaller --windowed --onedir --name "focus button" \
    --icon=icon.icns \
    --add-data "links.json:." \
    --add-data "alarm_sound.wav:." \
    main.py
```
6) Run the app

From Finder, open the project folder ```dist/focus-button/```.

Double click on the focus button.app icon <img width="12" height="12" alt="f__1_-removebg-preview" src="https://github.com/user-attachments/assets/c90c6fdc-5af7-4eb3-bc4f-cb86256f9222" />
 to launch.
