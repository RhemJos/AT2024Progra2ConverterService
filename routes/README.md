# 🐍 API REST - Converter Service

## 📂 Folder Structure

**Organizing the file structure to separate endpoint routes**

```
├── converters/          # Folder with converter folders
│   ├── audio_to_audio/
│   │   ├── audio_converter.py   
│   │   ├── audio_exception.py
│   │   └── audio_options.py
│   │
│   ├── compressor/           
│   │   └── compressor.py
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
├── routes/ 
│   └── [pending...]
│   
├── validators/ 
│   ├── Validator.py
│   └── VideoValidator.py
│
├── .dockerignore
├── .env.template
├── Dockerfile
├── README.md               # Repository documentation
├── app.py
├── docker-compose.yml
├── models.py
├── requirements.txt        # Project Dependencies
├── routes.py
└── utils.py
```


#### Folders and Files explanation 


```markdown
📁 converters/
[Pending]
- `**folders**`: [Pending]
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
