# Face Image Sorter

**Face Image Sorter** is a Python command-line tool that automatically sorts and filters images based on recognized faces.  
It uses the [`face_recognition`](https://github.com/ageitgey/face_recognition) library to compare images in a source folder against a set of known individuals, keeping only those with recognized matches.

---

## Features
- Load known faces from a directory structure.
- Compare faces in images against known individuals.
- Move matched images to a `keep` folder.
- Delete images without recognized faces.
- Adjustable matching tolerance for stricter or looser face recognition.
- Logs all actions to both the console and a log file.

---

## Installation

1. **Clone the repository**  
```bash
git clone https://github.com/YOUR_USERNAME/face-image-sorter.git
cd face-image-sorter
````

2. **Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

> **Note:** On Windows, installing `dlib` (required by `face_recognition`) can take a long time.
> To speed this up, you can install a prebuilt `dlib` wheel from [Gohlke's Python wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#dlib).

---

## Usage

**Command format:**

```bash
python sorter.py --source path/to/source_images --keep path/to/keep_folder --known path/to/known_faces --tolerance 0.6
```

**Arguments:**

* `--source` : Path to the directory containing images to process.
* `--keep` : Path to the directory where recognized images will be moved.
* `--known` : Path to the directory containing known individuals' images (organized by subfolder per person).
* `--tolerance` : Matching tolerance (default 0.6, lower = stricter).

**Example:**

```bash
python sorter.py --source ./unorganized_photos --keep ./sorted_photos --known ./known_people --tolerance 0.5
```

---

## Folder Structure for Known Faces

```
known_people/
│
├── Alice/
│   ├── alice1.jpg
│   ├── alice2.jpg
│
├── Bob/
│   ├── bob1.jpg
│   ├── bob2.png
```

---

## Log Output

All actions are logged in:

* `image_sorter.log`
* Console output

Example log entry:

```
2025-07-29 14:32:12 - INFO - KEPT: photo1.jpg (Recognized: Alice)
2025-07-29 14:32:15 - INFO - DELETED: random_image.png (No recognized faces)
```

---

## Requirements

* Python 3.7+
* face\_recognition
* dlib
* Pillow
* tqdm
* click
* numpy

Install them with:

```bash
pip install face_recognition pillow tqdm click numpy
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

Created by **Devansh Singh**

* [LinkedIn](https://www.linkedin.com/in/devansh-singh-amphitter/)
* [GitHub](https://github.com/amphitter)

````
