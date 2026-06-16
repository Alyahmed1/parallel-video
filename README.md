# Parallel Video Processing Pipeline
## Run
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py --in samples/input.mp4 --out out_serial.mp4
python run.py --in samples/input.mp4 --out out_parallel.mp4 --workers 2
