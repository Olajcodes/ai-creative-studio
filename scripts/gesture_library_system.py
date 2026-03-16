import os
import json
import subprocess
import librosa
import numpy as np
from typing import List, Dict, Optional
import whisper

class GestureLibrary:
    def init(self, library_path: str = "./gesture_library"):
        self.library_path = library_path
        self.gestures = []
        self.metadata_file = os.path.join(library_path, "gestures.json")
        os.makedirs(library_path, exist_ok=True)
        self.load_library()
    def load_library(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.gestures = json.load(f)
            print(f"Loaded {len(self.gestures)} gestures")
        else:
            self.create_default_library()

    def create_default_library(self):
        self.gestures = [
            {'id': 'neutral_talking', 'video': 'neutral_talking.mp4', 'semantic': 'neutral',
            'keywords': ['and', 'the', 'is', 'are'], 'emotion': 'neutral', 'duration': 5.0},
            {'id': 'nod_yes', 'video': 'nod_yes.mp4', 'semantic': 'agreement',
            'keywords': ['yes', 'correct', 'right', 'agree'], 'emotion': 'positive', 'duration': 2.5},
            {'id': 'shake_no', 'video': 'shake_no.mp4', 'semantic': 'disagreement',
            'keywords': ['no', 'not', 'wrong', 'disagree'], 'emotion': 'negative', 'duration': 2.0},
            {'id': 'shrug', 'video': 'shrug.mp4', 'semantic': 'uncertainty',
            'keywords': ['maybe', 'perhaps', 'unsure'], 'emotion': 'uncertain', 'duration': 3.0},
            {'id': 'point_right', 'video': 'point_right.mp4', 'semantic': 'direction_right',
            'keywords': ['right', 'there'], 'emotion': 'neutral', 'duration': 2.0},
            {'id': 'point_left', 'video': 'point_left.mp4', 'semantic': 'direction_left',
            'keywords': ['left', 'other'], 'emotion': 'neutral', 'duration': 2.0},
            {'id': 'thinking', 'video': 'thinking.mp4', 'semantic': 'contemplation',
            'keywords': ['think', 'consider', 'hmm'], 'emotion': 'contemplative', 'duration': 4.0},
            {'id': 'excited', 'video': 'excited.mp4', 'semantic': 'excitement',
            'keywords': ['great', 'amazing', 'wonderful'], 'emotion': 'excited', 'duration': 2.5},
            {'id': 'explaining', 'video': 'explaining.mp4', 'semantic': 'explanation',
            'keywords': ['because', 'so', 'therefore'], 'emotion': 'neutral', 'duration': 3.5},
            {'id': 'counting', 'video': 'counting.mp4', 'semantic': 'enumeration',
            'keywords': ['first', 'second', 'third'], 'emotion': 'neutral', 'duration': 2.0},
            {'id': 'emphasis', 'video': 'emphasis.mp4', 'semantic': 'emphasis',
            'keywords': ['important', 'crucial', 'must'], 'emotion': 'assertive', 'duration': 2.5},
            {'id': 'welcome', 'video': 'welcome.mp4', 'semantic': 'greeting',
            'keywords': ['hello', 'welcome', 'hi'], 'emotion': 'friendly', 'duration': 3.0}
        ]
        self.save_library()

    def save_library(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.gestures, indent=2, fp=f)

    def match_gesture_to_text(self, text: str, emotion: str = None) -> Dict:
        text_lower = text.lower()
        scores = []
        for gesture in self.gestures:
            score = sum(10 for kw in gesture['keywords'] if kw in text_lower)
            if emotion and emotion == gesture['emotion']:
                score += 5
            scores.append(score)
        return self.gestures[np.argmax(scores)] if max(scores) > 0 else self.get_neutral_gesture()

    def get_neutral_gesture(self) -> Dict:
        return next((g for g in self.gestures if g['id'] == 'neutral_talking'), self.gestures[0])

    def get_gesture_by_id(self, gesture_id: str) -> Optional[Dict]:
        return next((g for g in self.gestures if g['id'] == gesture_id), None)


class AudioAnalyzer:
    def init(self, model_size: str = "base"):
        print(f"Loading Whisper model: {model_size}")
        self.whisper_model = whisper.load_model(model_size)
    def extract_emotion(self, audio_path: str) -> str:
        y, sr = librosa.load(audio_path)
        energy = librosa.feature.rms(y=y)[0]
        return 'excited' if np.mean(energy) > 0.1 else 'neutral'

    def transcribe_audio(self, audio_path: str) -> Dict:
        return self.whisper_model.transcribe(audio_path, word_timestamps=True, verbose=False)

    def segment_by_sentences(self, audio_path: str) -> List[Dict]:
        result = self.transcribe_audio(audio_path)
        return [{'text': s['text'].strip(), 'start_time': s['start'], 
                'end_time': s['end'], 'duration': s['end'] - s['start']}
                for s in result['segments']]
        
        
class GestureVideoComposer:
    def init(self, gesture_library_path="./gesture_library",
        musetalk_path="./MuseTalk", temp_dir="./temp"):
        self.library = GestureLibrary(gesture_library_path)
        self.analyzer = AudioAnalyzer(model_size="base")
        self.musetalk_path = musetalk_path
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
    def create_gesture_sequence(self, audio_path, manual_timeline=None):
        if manual_timeline:
            return self._process_manual_timeline(manual_timeline, audio_path)
        return self._auto_generate_sequence(audio_path)

    def _auto_generate_sequence(self, audio_path):
        emotion = self.analyzer.extract_emotion(audio_path)
        segments = self.analyzer.segment_by_sentences(audio_path)
        print(f"Found {len(segments)} segments, emotion: {emotion}")
        
        return [{'gesture': self.library.match_gesture_to_text(s['text'], emotion),
                'text': s['text'], 'start_time': s['start_time'], 
                'end_time': s['end_time'], 'duration': s['duration'], 'segment_index': i}
                for i, s in enumerate(segments)]

    def _process_manual_timeline(self, timeline, audio_path):
        y, sr = librosa.load(audio_path)
        total_duration = len(y) / sr
        sequence = []
        
        for i, item in enumerate(timeline):
            gesture = self.library.get_gesture_by_id(item['gesture_id']) or self.library.get_neutral_gesture()
            end_time = timeline[i + 1]['time'] if i < len(timeline) - 1 else total_duration
            sequence.append({
                'gesture': gesture, 'text': item.get('text', ''),
                'start_time': item['time'], 'end_time': end_time,
                'duration': end_time - item['time'], 'segment_index': i
            })
        return sequence

    def preview_sequence(self, audio_path, manual_timeline=None):
        sequence = self.create_gesture_sequence(audio_path, manual_timeline)
        print("\n" + "="*80)
        print("GESTURE SEQUENCE PREVIEW")
        print("="*80 + "\n")
        for i, item in enumerate(sequence):
            print(f"Segment {i+1}:")
            print(f"  Time: {item['start_time']:.2f}s - {item['end_time']:.2f}s")
            print(f"  Gesture: {item['gesture']['id']}")
            print(f"  Text: \"{item['text']}\"")
            print()

    def compose_final_video(self, audio_path, output_path, avatar_image=None, manual_timeline=None):
        print("\n" + "="*60)
        print("GESTURE VIDEO COMPOSITION PIPELINE")
        print("="*60 + "\n")
        
        sequence = self.create_gesture_sequence(audio_path, manual_timeline)
        segment_videos = []
        
        for i, item in enumerate(sequence):
            audio_seg = os.path.join(self.temp_dir, f"audio_segment_{i}.wav")
            self._extract_audio_segment(audio_path, audio_seg, item['start_time'], item['duration'])
            
            gesture_video = os.path.join(self.library.library_path, item['gesture']['video'])
            seg_output = os.path.join(self.temp_dir, f"segment_{i}.mp4")
            
            try:
                self._generate_segment_video(gesture_video, audio_seg, seg_output, avatar_image)
                segment_videos.append(seg_output)
                print(f"  ✓ Segment {i+1}/{len(sequence)}")
            except Exception as e:
                print(f"  ✗ Segment {i+1} failed: {e}")
        
        self._concatenate_videos(segment_videos, output_path)
        print(f"\n✓ COMPLETE: {output_path}\n")
        return output_path

    def _generate_segment_video(self, gesture_video, audio_segment, output_path, avatar_image):
        input_source = gesture_video if os.path.exists(gesture_video) else avatar_image
        cmd = f"cd {self.musetalk_path} && python inference.py --video_path {input_source} --audio_path {audio_segment} --result_dir {os.path.dirname(output_path)} --fps 25 --batch_size 4"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"MuseTalk failed: {result.stderr}")

    def _extract_audio_segment(self, audio_path, output_path, start_time, duration):
        subprocess.run(f"ffmpeg -y -i {audio_path} -ss {start_time} -t {duration} -c copy {output_path}", 
                    shell=True, capture_output=True)

    def _concatenate_videos(self, video_list, output_path):
        concat_file = os.path.join(self.temp_dir, "concat_list.txt")
        with open(concat_file, 'w') as f:
            for video in video_list:
                f.write(f"file '{os.path.abspath(video)}'\n")
        subprocess.run(f"ffmpeg -y -f concat -safe 0 -i {concat_file} -c copy {output_path}", 
                    shell=True, capture_output=True)