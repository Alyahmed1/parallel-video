import numpy as np
from filters.core import pipeline
def test_pipeline_shape():
    img = np.zeros((64,64,3), dtype=np.uint8)
    out = pipeline(img)
    assert out.shape == img.shape
