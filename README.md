# 🏗 Python Coursework: Activity Installation & Run Guide

This guide explains which libraries are needed for each activity and how to run them professionally using Python 3.

---

## 🟢 Activity 1.1 – Student Marks

**How to run:**  
💻 Windows / macOS / Linux:  

```bash
cd ~/cousework/activity1_1
python3 student_marks.py
```
---

## 🟡 Activity 1.2 – Password Generator
**Libraries used:**  

**How to run:**  
```bash
cd ~/cousework/activity1_2  
python3 password_generator.py
```
---

## 🟠 Activity 1.3 – Graph & Route Validation

**How to run:**  
```bash
cd ~/cousework/activity1_3  
python3 route_planner.py
```
---

## 🔵 Activity 1.4 – Face Recognition


### Step 1: Install Libraries
💻 Windows / macOS / Linux (robust version):  

```bash
python3 -m pip install opencv-python
python3 -m pip install face_recognition
```

#### Windows Notes
- `face_recognition` depends on `dlib` (C++).
- If `pip install` fails, download the `.whl` file for your Python version from:  
  https://github.com/z-mahmud22/Dlib_Windows_Python3.x

- Install it locally:

- Then install `face_recognition`:

```bash
python3 -m pip install face_recognition
```

- Common fixes:
  - VSCode warning about `face_recognition_model`:

  ```bash
  python3 -m pip install setuptools
  ```

  - RGB/Grey image error:

  ```bash
  python3 -m pip uninstall numpy
  python3 -m pip install numpy==1.26.4
  ```



#### Mac Notes
- Install Homebrew first if it is not already installed.
- Then install `cmake` using Homebrew:

```bash
brew install cmake
python3 -m pip install face_recognition
```


- You may need to adjust the commands for your own machine. For example, use `python` instead of `python3` if your system does not use `python3`.


```

### Step 2: Run Activity
```bash
cd ~/cousework/activity1_4  
python3 activity1_4_parallel.py
```
