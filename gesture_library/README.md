# Gesture Library

## Required Gesture Videos

Place your gesture video files in this directory:

1. neutral_talking.mp4 - Natural talking, minimal gestures
2. nod_yes.mp4 - Nodding head for agreement
3. shake_no.mp4 - Shaking head for disagreement
4. shrug.mp4 - Shoulder shrug for uncertainty
5. point_right.mp4 - Pointing to the right
6. point_left.mp4 - Pointing to the left
7. thinking.mp4 - Hand on chin, contemplative
8. excited.mp4 - Excited hand gestures
9. explaining.mp4 - Open hand gestures while explaining
10. counting.mp4 - Counting on fingers
11. emphasis.mp4 - Strong hand gestures for emphasis
12. welcome.mp4 - Open arms welcoming gesture

## Recording Guidelines

- Duration: 2-5 seconds each
- Same person/avatar for all clips
- Same lighting and background
- Clear, frontal face visible
- Natural, loopable gestures
- 25-30 FPS
- Resolution: 720p or 1080p
- Format: MP4 (H.264)

## Usage

The gestures.json file will be auto-generated when you run the system.

## **Visual Directory Tree**
```
📁 /teamspace/studios/this_studio/
│
├─📁 MuseTalk/                     ← MuseTalk main code
│  ├─📁 models/                    ← Download models here
│  ├─📁 configs/
│  ├─📄 inference.py
│  └─📄 requirements.txt
│
├─📁 gesture_library/              ← YOUR GESTURE VIDEOS GO HERE
│  ├─🎬 neutral_talking.mp4
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
│  ├─📁 audio/                     ← Audio files here
│  │  ├─🔊 speech1.wav
│  │  └─🔊 speech2.wav
│  ├─📁 images/                    ← Avatar images (fallback)
│  │  └─🖼️ avatar.jpg
│  └─📁 videos/                    ← Optional full videos
│
├─📁 outputs/                      ← GENERATED VIDEOS
│  ├─🎬 final_video.mp4
│  └─📁 batch/
│
├─📁 temp/                         ← Temporary files (auto-cleaned)
│  ├─🔊 audio_segment_0.wav
│  └─🎬 segment_0.mp4
│
├─📁 scripts/                      ← Python scripts
│  ├─📄 gesture_library_system.py
│  ├─📄 generate_video.py
│  └─📄 batch_process.py
│
├─📁 configs/                      ← Configuration
│  ├─📄 timeline_example.json
│  └─📄 settings.yaml
│
└─📁 logs/                         ← Processing logs
   └─📄 processing.log

```
