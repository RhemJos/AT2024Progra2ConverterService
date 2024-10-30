# AT2024Progra2ConverterService

## Tablet of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies](#technologies)
- [Contributing](#contributing)

# Description

This project is an application offering multiple file conversion tools based on user needs. Users can upload files of various types (video, image, audio, etc.) and select the desired conversion type, such as converting videos to images, images to different formats, audio to text, among others. The project is built in Python using Flask as the framework for the REST API.

# Installation

## Requirements
- Python 3.9.0
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1

## Steps
1. Clone this repository locally:
   ```bash
   git clone https://github.com/jpsandovaln/AT2024Progra2ConverterService.git
   ```

2. Create and activate a virtual environment:
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

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

# Project Structure
The main project structure is as follows:
    ```graphql
    File-Converter-project/
    │
    ├── app/
    │   ├── __init__.py
    │   ├── routes.py
    │   ├── models.py
    │   ├── uploads/
    │   ├── converters/
    │   │   ├── video_to_images.py
    │   │   └── ...
    │   └── api/
    │       └── endpoints.py
    │
    ├── config.py
    ├── run.py
    ├── requirements.txt
    └── README.md
    ```

# Usage
To start the Flask server and run the application, use the following command:
    ```bash
    python run.py
    ```

# Api endpoints

# Technologies
- Backend: Python, Flask
- API Testing: Postman
- Virtual Environment: venv (Python virtual environment)
- Version Control: Git and GitHub

## Contributing

To contribute to this project:

1. **Fork the repository** on GitHub.
2. **Create a branch** for your feature or fix:
    ```bash
    git checkout -b feature-name
    ```
3. **Commit your changes** with a clear and descriptive message:
    ```bash
    git commit -m "Add new feature"
    ```
4. **Push the changes** to your forked repository:
    ```bash
    git push origin feature-name
    ```
5. **Open a Pull Request** on the original repository.