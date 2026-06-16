import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import cv2, argparse


def apply_filters(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def make_writer(out_path, fps, w, h):
    ext = os.path.splitext(out_path)[1].lower()
    if ext == ".avi":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
    else:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # for .mp4

    writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError(f"VideoWriter failed to open for {out_path}")
    return writer


def process_serial(in_path, out_path):
    cap = cv2.VideoCapture(in_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open input video: {in_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = make_writer(out_path, fps, w, h)

    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        writer.write(apply_filters(frame))
        count += 1

    cap.release()
    writer.release()
    print(f"Serial done: {count} frames")


if __name__ == "__main__":
    import multiprocessing as mp
    mp.freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", default="output.mp4")
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args()

    if args.workers <= 0:
        process_serial(args.inp, args.out)
    else:
        from pipeline.workers import process_parallel
        process_parallel(args.inp, args.out, args.workers, queue_size=8)
