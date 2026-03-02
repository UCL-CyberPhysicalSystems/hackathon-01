"""Test the inference engine locally without ROS2."""

import sys
import logging
from pathlib import Path
from PIL import Image as PILImage

# Add parent to path so we can import the engine
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inference import EmotionInferenceEngine


def main():
    logging.basicConfig(level=logging.INFO)
    # Load image
    
    script_dir = Path(__file__).resolve().parent
    image_path = script_dir / "test_image.png"


    image = PILImage.open(image_path).convert("RGB")
    print(f"Image size: {image.size}")

    # Create engine and run inference
    engine = EmotionInferenceEngine(
        model_id="dima806/facial_emotions_image_detection",
        device="cpu",
        top_k=3,
    )

    result = engine.predict(image)

    print("\n--- Prediction ---")
    print(f"  Top label:      {result['top_label']}")
    print(f"  Top confidence: {result['top_confidence']}")
    print(f"  All labels:     {result['labels']}")
    print(f"  All scores:     {result['confidences']}")
    print(f"  Inference time: {result['inference_ms']} ms")
    print(f"  Model:          {result['model_id']}")


if __name__ == "__main__":
    main()