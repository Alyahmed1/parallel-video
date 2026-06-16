import os
import cv2
import multiprocessing as mp


def apply_filters(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def _process_one(item):
    idx, frame = item
    out = apply_filters(frame)
    return idx, out


def _make_writer(out_path, fps, w, h):
    ext = os.path.splitext(out_path)[1].lower()
    if ext == ".avi":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
    else:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError(f"VideoWriter failed to open for {out_path}")
    return writer


def process_parallel(in_path, out_path, workers, queue_size=8):
    cap = cv2.VideoCapture(in_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open input video: {in_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Read all frames first (simple + reliable)
    frames = []
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append((idx, frame))
        idx += 1
    cap.release()

    if len(frames) == 0:
        raise RuntimeError("No frames read from input video.")

    writer = _make_writer(out_path, fps, w, h)

    # Process frames in parallel, but write in ORDER in main process
    with mp.Pool(processes=workers) as pool:
        for i, processed in pool.imap(_process_one, frames, chunksize=queue_size):
            writer.write(processed)

    writer.release()
    print(f"Parallel done: {len(frames)} frames with {workers} workers")
