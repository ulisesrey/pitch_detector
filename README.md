# Pitch Detector

Detect and visualize pitches from audio samples.

## Deployment
The app has been deployed on Railway. If I am still paying the subscription you can check it here: [https://pitchdetector.up.railway.app/](https://pitchdetector.up.railway.app/)

## Usage
If it's not available online or you want to test it locally, you can clone the repository and run it with:
```
uv run gunicorn --bind 0.0.0.0:8000 src.pitch_detector.app:app
```

Then open an internet browser like Firefox and copy http://0.0.0.0:8000 into the address bar.
You should see this:
![alt text](image-1.png)
Press "Start Recording" and say/sing something so the F0 frequency of that sound can be extracted and plotted.

The result would look something like this:


## Convert mp3 to wav
for f in *.mp3; do ffmpeg -i "$f" -acodec pcm_s16le -ar 22050 -ac 1 "${f%.mp3}.wav"; done

## Project Organization

```
├── data
│   ├── examples       <- Audio example of the Character Xiao.
│   ├── processed      <- The final, canonical data sets for modeling.
│   ├── raw            <- The original, immutable data dump.
│   └── sounds         <- The sounds from the original source
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── notebooks          <- Contains a notebook on f0 extraction using pyin.
│
├── reports
│   └── figures        <- Generated figures to be used in reporting
│
│
└── src               <- Source code for use in this project.
│    │
│    └── pitch_detector          <- pitch_detector Python module
│       ├── __init__.py
│       ├── app.py              <- Main app
│       ├── config.yaml         <- Store useful variables and configuration
│       ├── contour.py
│       ├── plots.py
│       ├── processing.py
│       ├── tones.py
│       ├── templates
│       │   └── index.html      <- front end html, contains js code  
│       └── uploads
│           └── recording.wav   <- uploaded audio file will be saved here
│   
├── .gitignore
├── Dockerfile      
├── LICENSE
├── Makefile          <- Makefile with convenience commands.
├── pyproject.toml    <- The central configuration file for the project.   
├── README.md         <- The top-level README for developers using this project.
├── uv.lock           <- The locked dependency file for reproducing the exact analysis environment
                         generated from `pyproject.toml` with the `uv lock` command.
```

--------

