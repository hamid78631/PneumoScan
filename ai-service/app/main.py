from fastapi import FastAPI , UploadFile, File
from PIL import Image
import numpy as np 
import io 
import tensorflow as tf 
from tensorflow.keras.applications.efficientnet import preprocess_input
import base64
import matplotlib.pyplot as plt

app = FastAPI()
MODEL_PATH = r"C:\Users\DELL\PneumoScan\ai-service\models\efficientnetb0_pneumonia.keras"
model = tf.keras.models.load_model(MODEL_PATH)
THRESHOLD = 0.25

@app.get("/")
def read_root():
    return {"status" : "Pneumoscan API en ligne"}


base_model = model.get_layer("efficientnetb0")
last_conv_layer_name = base_model.layers[-1].name

def make_gradcam_heatmap(img_array):
    last_conv_layer = base_model.get_layer(last_conv_layer_name)
    grad_model = tf.keras.models.Model(
        base_model.input, [last_conv_layer.output, base_model.output]
    )
    with tf.GradientTape() as tape:
        conv_output, base_output = grad_model(img_array)
        x = base_output
        for layer in model.layers[1:]:
            x = layer(x)
        class_channel = x[:, 0]

    grads = tape.gradient(class_channel, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_output = conv_output[0]
    heatmap = conv_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def overlay_heatmap(heatmap, original_img, alpha=0.4):
    heatmap = np.uint8(255 * heatmap)
    heatmap_img = Image.fromarray(heatmap).resize(original_img.size)
    heatmap_colored = plt.cm.jet(np.array(heatmap_img) / 255.0)[:, :, :3]
    heatmap_colored = np.uint8(255 * heatmap_colored)
    original_array = np.array(original_img)
    overlay = np.uint8(original_array * (1 - alpha) + heatmap_colored * alpha)
    return Image.fromarray(overlay)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    original_img = Image.open(io.BytesIO(contents)).convert("RGB").resize((224, 224))
    array = np.array(original_img, dtype=np.float32)
    array = preprocess_input(array)
    array = np.expand_dims(array, axis=0)

    score = float(model.predict(array)[0][0])
    label = "Pneumonie" if score > THRESHOLD else "Normal"

    heatmap = make_gradcam_heatmap(array)
    overlay_img = overlay_heatmap(heatmap, original_img)

    buffer = io.BytesIO()
    overlay_img.save(buffer, format="PNG")
    heatmap_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "label": label,
        "score": score,
        "heatmap": f"data:image/png;base64,{heatmap_base64}"
    }
