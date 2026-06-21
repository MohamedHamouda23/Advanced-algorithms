# 🏗 Advanced Algorithms Coursework

This project is part of the **Advanced Algorithms module (UWE Bristol)**. 
It focuses on implementing different activities using appropriate **data structures** and **algorithms** to support advanced algorithmic problem solving.

The coursework is designed to test understanding of:
- Efficient algorithm design 
- Data structure selection 
- Problem modelling 
- Performance optimisation

---

## 🟢 Activity 1.1 – Student Marks
This activity focuses on building a data processing and analytics system that calculates final degree classifications for students. It tests your ability to apply weighted averages, handle structured data from CSV files, and implement algorithmic logic based on real academic regulations.



**How to run:**  
💻 Windows / macOS / Linux:  

```bash
cd ~/cousework/activity1_1
python3 student_marks.py
```
---

## 🟡 Activity 1.2 – Password Generator
This activity evaluates your ability to generate constrained combinatorial outputs using algorithmic search techniques. You are expected to apply brute-force or optimised generation strategies while enforcing multiple logical constraints.

**How to run:**  
```bash
cd ~/cousework/activity1_2  
python3 password_generator.py
```
---

## 🟠 Activity 1.3 – Graph & Route Validation
This activity involves solving a constrained optimisation problem on a weighted graph. You are required to design an algorithm that finds the lowest-cost route across a network while respecting visitation constraints.

**How to run:**  
```bash
cd ~/cousework/activity1_3  
python3 route_planner.py
```
---

## 🔵 Activity 1.4 – Face Recognition
This activity focuses on performance optimisation using parallel programming techniques. You are required to improve a sequential image processing system by introducing concurrency to reduce execution time.


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
