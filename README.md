# Frame Extractor

This is a simple Python application that extracts frames from a video file. It uses OpenCV for frame extraction and PyQt5 for the user interface.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.6 or later.
- You have installed the required Python packages. You can install them using pip:

```bash
pip install -r requirements.txt
```

## Using Frame Extractor

To use Frame Extractor, follow these steps:

1. Run the script:

```bash
python main.py
```

2. In the application window, click “Select Video” and choose a video file.
3. Click “Select Output Folder” and choose an output folder.
4. Click “Extract Frames” to start the frame extraction process.

The application will create a new folder in the output folder for each video, and save the extracted frames as `.jpg` files in this folder.
