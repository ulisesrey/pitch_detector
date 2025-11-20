# Pitch Detector

A web application for real-time fundamental frequency (F0) extraction and visualization, originally designed to help Chinese learners analyze and practice pronunciation tones.

## Deployment
The app is available [here](https://pitchdetector.up.railway.app/)

If it's not available online or you want to test it locally, you can clone the repository and run it with:
```
uv run gunicorn --bind 0.0.0.0:8000 src.pitch_detector.app:app
```

Then open an internet browser like Firefox and copy http://0.0.0.0:8000 into the address bar.

## Usage

You should see this:
![alt text](website_example.png)
Press "Start Recording" and say/sing/play something so the F0 frequency of that sound can be extracted and plotted.

The result would look something like this:
![alt text](pitch_example.png)

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
└── src                <- Source code for use in this project.
│    │
│    └── pitch_detector         <- pitch_detector Python module
│       ├── templates
│       │   └── index.html      <- front end html, contains js code 
│       ├── tests
│       │   └── test_all.py     <- Contains tests
│       ├── uploads
│       │   └── recording.wav   <- uploaded audio file will be saved here
│       ├── __init__.py
│       ├── app.py              <- Main app
│       ├── config.yaml         <- Store useful variables and configuration
│       ├── contour.py
│       ├── plots.py
│       ├── processing.py
│       └── tones.py
│   
├── .gitignore
├── Dockerfile      
├── LICENSE
├── Makefile          <- Makefile with convenience commands.
├── pyproject.toml    <- The central configuration file for the project.   
├── README.md         <- The top-level README for developers using this project.
└── uv.lock           <- The locked dependency file for reproducing the exact analysis environment
                         generated from `pyproject.toml` with the `uv lock` command.
```

## Motivation

As I started learning Chinese I was very interested in the tones in Chinese language. In Chinese, words have tones, and the same spelling but with different tone can mean different things. For example the word "ma" depending on which tone, can mean different words like "mother", "numb", "horse" or "to scold". For people who learn a language with tones for the first time this can be challenging. I watched many videos to hear the difference [[1]](https://www.youtube.com/watch?v=RRaHXPDIV-4) [[2]](https://www.youtube.com/shorts/AT9-FQuJ6DQ) and understood that the first tone (  ̄ ) is high pitched, the second one (  ́ ) is ascending, the third one (  ̌ ) going down and then up, the fourth one (  ̀ ) going down, and lastly the neutral one.
```
Tone 1 ( ̄): mā, mother
Tone 2 ( ́): má, numb
Tone 3 ( ̌): mǎ, horse
Tone 4 ( ̀): mà, to scold
Tone 5 (neutral): ma, used as a question particle
```

Often this is depicted in a figure like this one:
![alt text](tone_graph.png)

I wanted to:
1.  See how real data, real words spoken in chinese would look on a pitch graph
2.  See if I could pronounce the words correcly not just by hearing at them, but by looking at how their pitch profile looks like.

For 1. I extracted the Fundamental Frequency (F₀) of the Anki Dataset [800 Basic Chinese Characters](https://ankiweb.net/shared/info/1443941528) which contains the Hanzi, the pinyin and the sound of 800 chinese characters. You can find the data in [data](https://github.com/ulisesrey/pitch_detector/tree/main/data). 

For 2. I created the app to record the sound and plot the F₀.

## Results
Indeed, by analzying the fundamental frequency of each sound file and grouping them according to their tone I could obtain beautiful pitch curves very similar to the theoretical ones.
![alt text](Figure_1.png)
Notes:
*Audio files were not aligned on the temporal axis, so they do not start exactly at the same time. Some files contained two pronunciation variants of the same Hanzi in the same audio file, only the first one is shown.* 

## Methods

### Convert mp3 to wav
The original mp3 files were converted to wav, with ffmpeg. This was needed for librosa to read the audio files, since mp3 is not supported.
```
for f in *.mp3; do ffmpeg -i "$f" -acodec pcm_s16le -ar 22050 -ac 1 "${f%.mp3}.wav"; done
```

### Data Processing
The ankicard dataset was exported to a .txt file and processed with the processing.py module.

### F₀ extraction
Extraction of the Fundamental Frequency (F₀) was performed with the librosa library using the ```librosa.pyin()``` function.

## Further development
Check the issues and add one if you would like to add a feature to this project.
