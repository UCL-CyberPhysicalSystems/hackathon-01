from transformers import pipeline as hf_pipeline
from PIL import Image as PILImage
import numpy as np
import time
import logging

logger = logging.getLogger(__name__)


class EmotionInferenceEngine:
    """wrap pipeline"""

    def __init__(
        self,
        model_id: str = "dima806/facial_emotions_image_detection",
        device: str = "cpu",
        top_k: int = 3,
        max_retries: int = 3,
    ):
        self.model_id = model_id
        self.device = device
        self.top_k = top_k
        self.pipeline = None
        self._load_model(max_retries)

    def _load_model(self, max_retries: int) -> None:
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Loading model (attempt {attempt}/{max_retries}): {self.model_id}")
                self.pipeline = hf_pipeline(
                    "image-classification",
                    model=self.model_id,
                    device=-1 if self.device == "cpu" else 0,
                )
                logger.info("Model loaded successfully.")
                return
            except Exception as e:
                logger.error(f"Model load failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                else:
                    raise RuntimeError(f"Could not load model after {max_retries} retries") from e

    def predict(self, image) -> dict:
        """
        run inference on single image

        input can be PIL or numpy, output is dict with:
        - top_label
        - top_confidence
        - labels (list)
        - confidences (list)
        - inference_ms
        """
        if self.pipeline is None:
            raise RuntimeError("Pipeline not loaded")

        # Convert numpy to PIL if needed
        if isinstance(image, np.ndarray):
            pil_image = PILImage.fromarray(image)
        else:
            pil_image = image

        t_start = time.monotonic()
        results = self.pipeline(pil_image, top_k=self.top_k)
        inference_ms = (time.monotonic() - t_start) * 1000.0

        labels = [r["label"] for r in results]
        confidences = [round(r["score"], 4) for r in results]

        return {
            "top_label": labels[0],
            "top_confidence": confidences[0],
            "labels": labels,
            "confidences": confidences,
            "inference_ms": round(inference_ms, 2),
        }