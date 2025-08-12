import io

import torch
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

# Load YOLOv7 model (đặt model.pt cùng thư mục app.py)
model = torch.hub.load('WongKinYiu/yolov7', 'custom', 'best.pt', force_reload=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/detect')
async def detect_board(file: UploadFile = File(...)):
    print("Received file:", file.filename, file.content_type)
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    # Lưu ảnh nhận được từ app ra file để kiểm tra
    image.save("received_from_app.jpg")
    print("Image size:", image.size, "mode:", image.mode)
    results = model(image)
    df = results.pandas().xyxy[0]
    print("Detection dataframe:\n", df)
    # Trả về dataframe thô để debug
    if not df.empty:
        labels = df['name'].tolist() if 'name' in df.columns else []
        print("Detected labels:", labels)
        return {"result": ', '.join(labels), "raw": df.to_dict()}
    return {"result": "Không nhận diện được board!", "raw": df.to_dict()}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

let result = await ImagePicker.launchImageLibraryAsync({
  mediaTypes: ImagePicker.MediaTypeOptions.Images,
  allowsEditing: true,
  quality: 1,
  // KHÔNG thêm base64: true
});
if (!result.canceled && result.assets.length > 0) {
  setImage(result.assets[0].uri); // uri phải là file path
}
