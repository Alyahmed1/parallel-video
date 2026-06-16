# Parallel Video Processing Pipeline

Benchmarks serial vs. parallel video frame processing with OpenCV. Each frame goes through a grayscale → Gaussian blur → Canny edge detection filter; the parallel mode distributes frames across multiple worker processes (via `multiprocessing.Pool`) while preserving original frame order in the output video.

## Run
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py --in samples/input.mp4 --out out_serial.mp4
python run.py --in samples/input.mp4 --out out_parallel.mp4 --workers 2
