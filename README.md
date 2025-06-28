# yt-dlp GUI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A clean, modern, and user-friendly Graphical User Interface for the `yt-dlp` command-line tool. Download videos and audio from YouTube.

![Screenshot of the yt-dlp GUI application](screenshot.png)  

---

## Features

- **Simple Interface**: Just paste a URL, choose your options, and click download.
- **Video & Audio**: Download full videos or extract audio into MP3 or lossless WAV files.
- **Quality Selection**: Choose your preferred video resolution or audio bitrate.
- **Real-Time Progress**: A progress bar and detailed log keep you updated on the download status.
- **Modern Look**: Built with `ttkbootstrap` for a good look and feel on any OS.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.8+**
2.  **FFmpeg**: This is **needed** for `yt-dlp` to download high-quality streams and convert audio.
    -   **Windows**: Download a build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add the `bin` folder to your system's PATH.
    -   **macOS (Homebrew)**: `brew install ffmpeg`
    -   **Linux (Debian/Ubuntu)**: `sudo apt update && sudo apt install ffmpeg`

## Installation Guide

Follow the instructions for your specific operating system.

### macOS Instructions

These instructions assume you have [Homebrew](https://brew.sh), the standard package manager for macOS.

1.  **Install Prerequisites with Homebrew**:
    If you don't have Homebrew, [install it first](https://brew.sh). Then, open your Terminal and run:
    ```bash
    brew install python git ffmpeg
    ```

2.  **Clone the Repository**:
    Navigate to where you want to store the project and run:
    ```bash
    git clone https://github.com/YourUsername/yt-dlp-gui.git
    cd yt-dlp-gui
    ```

3.  **Create a Virtual Environment**:
    This is highly recommended to keep dependencies separate.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    (Your terminal prompt should now show `(venv)` at the beginning).

4.  **Install Python Packages**:
    Install all the required packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    ## Usage

Once the installation is complete, run the application with:

```bash
python ytdlp_gui.py
```

### Linux (Debian/Ubuntu) Instructions

These instructions are for Debian-based distributions like Ubuntu, Mint, Pop!_OS, etc. For other distributions (Fedora, Arch), use their respective package managers (`dnf`, `pacman`).

1.  **Install Prerequisites with apt**:
    Open your terminal and run the following commands to get `git`, `python`, and `ffmpeg`.
    ```bash
    sudo apt update
    sudo apt install git python3 python3-pip python3-venv ffmpeg -y
    ```
    *(Note: `python3-venv` is a required package on Debian/Ubuntu for creating virtual environments).*

2.  **Clone the Repository**:
    Navigate to where you want to store the project and run:
    ```bash
    git clone https://github.com/YourUsername/yt-dlp-gui.git
    cd yt-dlp-gui
    ```

3.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    (Your terminal prompt should now show `(venv)` at the beginning).

4.  **Install Python Packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once the installation is complete, run the application with:

```bash
python ytdlp_gui.py
```

### Windows Instructions

1.  **Install Prerequisites**:
    - **Python**: Download and install from the [official Python website](https://www.python.org/downloads/). **Make sure to check the "Add Python to PATH" box** during installation.
    - **Git**: Download and install [Git for Windows](https://git-scm.com/download/win).
    - **FFmpeg**: This is **essential**. Download a build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (get the `full_build.zip`). Unzip it, and you will see a `bin` folder inside. You must add this `bin` folder's location to your system's PATH environment variable.

2.  **Clone the Repository**:
    Open Command Prompt or PowerShell and navigate to where you want to store the project.
    ```powershell
    git clone https://github.com/YourUsername/yt-dlp-gui.git
    cd yt-dlp-gui
    ```

3.  **Create a Virtual Environment**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

4.  **Install Python Packages**:
    ```powershell
    pip install -r requirements.txt
    ```
---

## Usage

After completing the installation for your OS, make sure your virtual environment is activated, then run the application with:

```bash
python ytdlp_gui.py
