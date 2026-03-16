# MuseTalk Gesture Library System - Setup Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## 🎯 Overview

This system combines **MuseTalk** (audio-driven lip-sync) with a **Gesture Library** to create realistic talking head videos with semantically matched gestures. The system prevents gesture-audio mismatch (e.g., nodding while saying "no") by intelligently matching gestures to speech content.

### Key Features
- ✅ Audio-driven lip synchronization
- ✅ Semantic gesture-audio alignment
- ✅ Manual or automatic gesture selection
- ✅ Batch processing support
- ✅ Emotion detection from audio
- ✅ Reusable gesture library

---

## 🔧 Prerequisites

### System Requirements
- **Platform**: Lightning AI Studio (recommended) or Ubuntu 22.04+
- **GPU**: A10G, A100, or similar (CUDA-enabled)
- **RAM**: 16GB+ recommended
- **Storage**: 15GB+ free space
- **Python**: 3.8, 3.9, or 3.10

### Required Tools
- Git
- FFmpeg
- Python pip

### Lightning AI Account
- Sign up at [lightning.ai](https://lightning.ai)
- Create a new Studio with GPU support

---

## 🚀 Installation

### Step 1: Access Lightning AI Terminal

1. Log in to Lightning AI
2. Open your Studio
3. Click on **Terminal** to access the command line

### Step 2: Run Installation Script

Copy and paste the following commands into the Lightning AI terminal:
```bash
# Navigate to workspace
cd /teamspace/studios/this_studio/ai-creative-studio

# Create main directory structure
mkdir -p MuseTalk
mkdir -p gesture_library
mkdir -p inputs/{audio,images,videos}
mkdir -p outputs/batch
mkdir -p temp
mkdir -p scripts
mkdir -p configs
mkdir -p logs


# Install MuseTalk dependencies
cd MuseTalk
pip install -r requirements.txt

# Install additional dependencies for Gesture System
pip install openai-whisper --break-system-packages
pip install librosa soundfile --break-system-packages
pip install nltk --break-system-packages

# Return to main directory
/teamspace/studios/this_studio/ai-creative-studio
```

### Step 3: Download MuseTalk Models
```bash
cd /teamspace/studios/this_studio/ai-creative-studio/MuseTalk

# Download model weights (this may take 5-10 minutes)
bash scripts/download_models.sh

# Or download manually from GitHub releases if script fails:
# https://github.com/TMElyralab/MuseTalk/releases
```

### Step 4: Verify Installation
```bash
# Check directory structure
cd /teamspace/studios/this_studio/ai-creative-studio
ls -la

# Expected directories:
# MuseTalk/
# gesture_library/
# inputs/
# outputs/
# temp/
# scripts/
# configs/
# logs/
```

---

## 📁 Directory Structure
```
📁 /teamspace/studios/this_studio/ai-creative-studio
│
├─📁 MuseTalk/                     ← MuseTalk main code
│  ├─📁 models/                    ← Model weights (auto-downloaded)
│  ├─📁 configs/                   ← MuseTalk configurations
│  ├─📄 inference.py               ← Main inference script
│  └─📄 requirements.txt           ← Python dependencies
│
├─📁 gesture_library/              ← YOUR GESTURE VIDEOS GO HERE
│  ├─🎬 neutral_talking.mp4        ← Upload these 12 videos
│  ├─🎬 nod_yes.mp4
│  ├─🎬 shake_no.mp4
│  ├─🎬 shrug.mp4
│  ├─🎬 point_right.mp4
│  ├─🎬 point_left.mp4
│  ├─🎬 thinking.mp4
│  ├─🎬 excited.mp4
│  ├─🎬 explaining.mp4
│  ├─🎬 counting.mp4
│  ├─🎬 emphasis.mp4
│  ├─🎬 welcome.mp4
│  └─📄 gestures.json              ← Auto-generated metadata
│
├─📁 inputs/                       ← YOUR INPUT FILES
│  ├─📁 audio/                     ← Place audio files here
│  ├─📁 images/                    ← Avatar images (fallback)
│  └─📁 videos/                    ← Optional full videos
│
├─📁 outputs/                      ← GENERATED VIDEOS APPEAR HERE
│  └─📁 batch/                     ← Batch processing outputs
│
├─📁 temp/                         ← Temporary processing files
├─📁 scripts/                      ← Python scripts
├─📁 configs/                      ← Configuration files
└─📁 logs/                         ← Processing logs
```

---

## ⚙️ Configuration

### Required Gesture Videos

Upload these 12 videos to `gesture_library/`:

| Gesture ID | Filename | Description |
|------------|----------|-------------|
| neutral_talking | neutral_talking.mp4 | Natural talking, minimal gestures |
| nod_yes | nod_yes.mp4 | Nodding head for agreement |
| shake_no | shake_no.mp4 | Shaking head for disagreement |
| shrug | shrug.mp4 | Shoulder shrug for uncertainty |
| point_right | point_right.mp4 | Pointing to the right |
| point_left | point_left.mp4 | Pointing to the left |
| thinking | thinking.mp4 | Hand on chin, contemplative |
| excited | excited.mp4 | Excited hand gestures |
| explaining | explaining.mp4 | Open hand gestures |
| counting | counting.mp4 | Counting on fingers |
| emphasis | emphasis.mp4 | Strong hand gestures |
| welcome | welcome.mp4 | Open arms welcoming |

**Video Requirements:**
- Duration: 2-5 seconds each
- Same person/avatar for all clips
- Same lighting and background
- Clear, frontal face visible
- 25-30 FPS, 720p or 1080p
- MP4 format (H.264 codec)

---

## 🎬 Usage

### Quick Start

1. **Upload your files:**
   - Gesture videos → `gesture_library/`
   - Audio file → `inputs/audio/`
   - Avatar image → `inputs/images/` (optional)

2. **Create timeline** (in Python):
```python
manual_timeline = [
    {'time': 0.0, 'gesture_id': 'welcome', 'text': 'Hello everyone!'},
    {'time': 3.5, 'gesture_id': 'nod_yes', 'text': 'Yes, this is correct'},
    {'time': 7.0, 'gesture_id': 'shake_no', 'text': 'No, that won\'t work'},
    {'time': 11.0, 'gesture_id': 'excited', 'text': 'Amazing results!'}
]
```

3. **Generate video:**
```python
from scripts.gesture_library_system import GestureVideoComposer

composer = GestureVideoComposer()
composer.compose_final_video(
    audio_path="./inputs/audio/speech.wav",
    output_path="./outputs/final_video.mp4",
    avatar_image="./inputs/images/avatar.jpg",
    manual_timeline=manual_timeline
)
```

4. **Download result** from `outputs/` folder

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| **CUDA Out of Memory** | Reduce `batch_size` to 4 or 2 in settings |
| **Gesture videos not found** | Verify uploads in `gesture_library/` |
| **Face not detected** | Use clear frontal face images/videos |
| **Audio sync issues** | Convert audio to 16kHz WAV format |
| **Model weights missing** | Run `bash scripts/download_models.sh` |

---

## 📝 Next Steps

1. ✅ Upload 12 gesture videos
2. ✅ Upload audio file
3. ✅ Create manual timeline
4. ✅ Generate first test video
5. ✅ Review and refine
6. ✅ Scale to production

---

## 📚 Resources

- [MuseTalk Repository](https://github.com/TMElyralab/MuseTalk)
- [Lightning AI Docs](https://lightning.ai/docs)
- [Whisper AI](https://github.com/openai/whisper)

---

## ✅ Setup Checklist

- [ ] Lightning AI account created
- [ ] Studio with GPU launched
- [ ] Installation script executed
- [ ] MuseTalk models downloaded
- [ ] 12 gesture videos uploaded
- [ ] Test audio file uploaded
- [ ] First test video generated
- [ ] System understood and ready for use

---

**Version**: 1.0  
**Last Updated**: 2024
