# AT2024Progra2ConverterService
# 🐍 Converter Service

# Description
This project provides a variety of file conversion tools. Users can upload files of various types (video, image, audio, etc.) and choose specific processing tasks, such as extracting images (frames) from a video, converting an image to different formats, or changing its properties, among other options. The project is developed in Python, with Flask serving as the framework for the REST API.

## Tablet of Contents

- [Project Structure](#-project-structure)
- [Installation](#installation)
- [Folder and Files explanation](#folders-and-files-explanation-)


# 📂 Project Structure


```
├── converters/          # Folder with converter folders
│   ├── audio_to_audio/
│   │   ├── audio_converter.py   
│   │   ├── audio_exception.py
│   │   └── audio_options.py
│   │
│   ├── extractor/
│   │   ├── bin/exifTool/
│   │   │   └── [corresponding files...]
│   │   │
│   │   ├── extractor.py
│   │   └── metadataextractor.py
│   │   
│   ├── image_to_image/
│   │   └── image_converter.py
│   │   
│   ├── video_to_images/
│   │   └── video_to_images.py
│   │   
│   ├── video_to_video/
│   │   └── video_to_video.py
│   │   
│   └── converter.py
│   
├── helpers/           
│   ├── compressor.py
│   ├── endpoints_helper.py
│   └── utils.py
│   
├── routes/ 
│   ├── audio_routes.py
│   ├── download_routes.py
│   ├── image_routes.py
│   ├── login_routes.py
│   ├── metadata_routes.py
│   └── video_routes.py
│   
├── validators/ 
│   ├── Validator.py
│   └── VideoValidator.py
│
├── .dockerignore
├── .env.template
├── app.py
├── docker-compose.yml
├── Dockerfile
├── models.py
├── README.md               # Repository documentation
├── requirements.txt        # Project Dependencies
├── routes.py
└── utils.py
```

# Installation

## Steps
**1. Clone this repository locally:**
   ```bash
   git clone https://github.com/jpsandovaln/AT2024Progra2ConverterService.git
   ```

**2. Create and activate a virtual environment:**
* On Windows:
 ```bash
 python -m venv venv
 venv\Scripts\activate
 ```
* On Linux:
 ```bash
 python -m venv venv
 source myenv/bin/activate
 ```

**3. Install the required dependencies:**

To view all the packages and dependencies needed to run this project, check the requirements.txt file. You can install them easily with the following command
```bash
pip install -r requirements.txt
```
Git LFS must also be installed with the following command
```bash
git lfs install
```

# Folders and Files explanation 

```markdown
📁 converters/
[Pending]
- `**folders**`: [Pending]
- `**files**.py`: [Pending]

📁 helpers/
[Pending]
- `**files**.py`: [Pending]

📁 routes/
[Pending]
- `**files**.py`: [Pending]

📁 validators/
[Pending]
- `**files**.py`: [Pending]

📄 `.dockerignore`: [Pending]
📄 `.env.template`: [Pending]
📄 `.Dockerfile`: [Pending]
📄 `README.md`: Repository documentation
📄 `app.py`: [Pending]
📄 `docker-compose.yml`: [Pending]
📄 `models.py`: [Pending]
📄 `requirements.txt`: [Pending]
📄 `routes.py`: [Pending]
📄 `utils.py`: [Pending]
```
