import os, sys, time, wave, tempfile, random, collections
import numpy as np
import pyaudio, webrtcvad, librosa, tensorflow as tf
import tensorflow as tf
from tensorflow import keras
import edge_tts
import csv
import asyncio
from keras import layers, models
from pathlib import Path
from CommonUtil import read_key_from_JSON, JSON_config_changer
import soundfile as sf
Debugstat = read_key_from_JSON("Udebug")
Ubotreference = read_key_from_JSON("Ubotreference")
csv_file = 'voices_parsed.csv'
"""
Keyword + VAD Spotter (TensorFlow 2.12 macOS)
- Uses your voice clips in ./WWD_DB as positives (keyword by your voice)
- Generates negatives (noise/silence) automatically
- Augments your own voice (stretch, pitch, noise)
- First run: auto-trains; later runs: listens via WebRTC VAD + PyAudio
- Saves detected fragments to ./captures

Install (macOS):
  brew install portaudio       # for PyAudio build
  pip install pyaudio webrtcvad librosa soundfile numpy
  pip install tensorflow-macos==2.12.0

Notes for TF 2.12:
- Use H5 format for saving models to avoid newer Keras format issues
"""
# === Global config ===
async def main(infov, language, filename):
    tts = edge_tts.Communicate(text=(infov), voice=language)
    try:
        await tts.save(filename)
    except Exception as e:
        pass

def teach_international():
    import os
    # Получаем путь к папке, где находится текущий скрипт
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Добавляем к нему папку WWD_DB
    wwd_db_path = os.path.join(base_dir, "WWD_DB")
    from datetime import datetime
    if not os.path.exists(wwd_db_path):
        os.makedirs(wwd_db_path)
    current_model = 0
    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                now = datetime.now()
                filename = now.strftime("audio_%Y%m%d_%H%M%S_%f.wav")
                filename = os.path.join(wwd_db_path, filename)
                shortname = (row["ShortName"])
                asyncio.run(main(Ubotreference, shortname, filename))
                current_model += 1
                progress = int((current_model * 100) / 302)
                print(f"\rData collected: {progress}%", end="", flush=True)
    except Exception as e:
        print(f"⚠️ Ошибка при поиске shortname: {e}")
    

Debugstat = True
SAMPLE_RATE = 16000
CLIP_DURATION = 1.0
N_MFCC = 40
N_FFT = 512
HOP_LENGTH = 160
KWS_THRESHOLD = 0.85
KEYWORD = read_key_from_JSON("Ubotreference")  # read_key_from_JSON("Ubotreference")

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent  # поднялись на 3 уровня вверх

MD_folder = project_root / "AImodels"
MODEL_PATH = MD_folder / "kws_model.h5" # H5 for TF 2.12 compatibility

# === Features ===
def mfcc_features(y, sr, max_len=32):
    if y.dtype != np.float32:
        y = y.astype(np.float32)
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC, n_fft=N_FFT, hop_length=HOP_LENGTH)
    m = (m - np.mean(m)) / (np.std(m) + 1e-6)
    m = m.T  # (time, n_mfcc)
    
    # фиксируем длину по time
    if m.shape[0] < max_len:
        pad_width = max_len - m.shape[0]
        m = np.pad(m, ((0,pad_width),(0,0)), mode='constant')
    elif m.shape[0] > max_len:
        m = m[:max_len, :]
    
    return np.expand_dims(m, axis=-1)  # (time, n_mfcc, 1)

# === Augmentation ===
def augment_audio(y, sr):
    y = y.astype(np.float32, copy=False)
    choice = random.choice(["noise", "stretch", "pitch", "none"])
    
    try:
        if choice == "noise":
            y = y + 0.005 * np.random.randn(len(y)).astype(np.float32)
        elif choice == "stretch":
            rate = float(np.random.uniform(0.9, 1.1))
            y = librosa.effects.time_stretch(y, rate=rate)
        elif choice == "pitch":
            steps = int(random.randint(-2, 2))
            if steps != 0:
                y = librosa.effects.pitch_shift(y, sr=sr, n_steps=steps)
    except Exception as e:
        if Debugstat is True:
            print("Ошибка аугментации:", e)
    
    # вручную подгоняем длину
    target_len = int(CLIP_DURATION * SAMPLE_RATE)
    if len(y) < target_len:
        y = np.pad(y, (0, target_len - len(y)), mode='constant')
    elif len(y) > target_len:
        y = y[:target_len]

    return y

# === Data loading ===
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "WWD_DB")
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Папка с данными не найдена: {data_dir}")

    X, y = [], []
    wavs = [f for f in os.listdir(data_dir) if f.lower().endswith('.wav')]
    if len(wavs) == 0:
        raise RuntimeError("В папке WWD_DB нет .wav файлов.")
    for file in wavs:
        if "augmented" in file.lower():
            continue
        path = os.path.join(data_dir, file)
        audio, sr = librosa.load(path, sr=SAMPLE_RATE, mono=True)
        
        # baseline keyword
        X.append(mfcc_features(audio, sr))
        y.append(1)

        # аугментации
        for i in range(5):
            aug = augment_audio(audio, sr)
            aug_filename = os.path.join(data_dir, f"{os.path.splitext(file)[0]}_augmented_{i}.wav")
            sf.write(aug_filename, aug, sr)
            X.append(mfcc_features(aug, sr))
            y.append(1)

    # Negatives = random noise
    neg_count = max(len(X), 64)
    for _ in range(neg_count):
        noise = (0.01 * np.random.randn(int(CLIP_DURATION * SAMPLE_RATE))).astype(np.float32)
        X.append(mfcc_features(noise, SAMPLE_RATE))
        y.append(0)

    # Negatives = silence
    for _ in range(neg_count):
        silence = np.zeros(int(CLIP_DURATION * SAMPLE_RATE), dtype=np.float32)
        X.append(mfcc_features(silence, SAMPLE_RATE))
        y.append(0)

        # слегка "шумная тишина"
        silence_noise = 0.001 * np.random.randn(int(CLIP_DURATION * SAMPLE_RATE)).astype(np.float32)
        X.append(mfcc_features(silence_noise, SAMPLE_RATE))
        y.append(0)

    X = np.asarray(X)
    y = np.asarray(y, dtype=np.float32)
    return X, y

# === Model ===
def build_model(input_shape):
    model = models.Sequential([
        layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# === Train ===
def train():
    if Debugstat is True:
        print("WWD is loading...")
    teach_international()
    X, y = load_data()
    if Debugstat is True:
        print(f"⚙️ Обучаю модель на {len(X)} примерах...")
    model = build_model(X.shape[1:])

    # веса классов (ключевое слово ценнее)
    class_weight = {0: 1.0, 1: 3.0}

    model.fit(X, y, epochs=15, batch_size=16, validation_split=0.2, class_weight=class_weight, verbose=1)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save(MODEL_PATH)  # TF 2.12 will save as H5 because path endswith .h5
    if Debugstat is True:
        print(f"✅ Модель сохранена: {MODEL_PATH}")
    # JSON_config_changer("Trained_AMO", len(X))

