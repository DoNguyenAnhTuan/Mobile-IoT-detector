# app.py
import io

import pandas as pd
import torch
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image

# Tải model 1 lần khi khởi động (đặt best.pt cùng thư mục)
model = torch.hub.load(
    'WongKinYiu/yolov7',
    'custom',
    'best.pt',          # hoặc path='best.pt' tùy hubconf
    force_reload=False, # True nếu muốn buộc tải lại repo mỗi lần khởi động
    trust_repo=True
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}


@app.post("/detect")
async def detect_board(file: UploadFile = File(...)):
    try:
        print("[DEBUG] file:", file)
        if not file:
            print("[ERROR] Không nhận được file từ client!")
            return JSONResponse(status_code=400, content={"error": "Không nhận được file từ client!"})
        print(f"[DEBUG] file.filename: {file.filename}, file.content_type: {file.content_type}")
        contents = await file.read()
        if not contents or len(contents) < 10:
            print("[ERROR] File rỗng hoặc quá nhỏ!")
            return JSONResponse(status_code=400, content={"error": "File rỗng hoặc không hợp lệ!"})
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except Exception as e:
            print("[ERROR] Không mở được ảnh:", e)
            return JSONResponse(status_code=400, content={"error": "Không mở được ảnh: " + str(e)})
        image.save("received_from_app.jpg")  # debug

        results = model(image)

        # YOLOv5/7 style: ưu tiên .pandas(); fallback nếu môi trường thiếu
        try:
            df = results.pandas().xyxy[0]
        except Exception:
            # Fallback parse tensor
            import numpy as np
            names = getattr(results, "names", [])
            arr = results.xyxy[0].cpu().numpy()  # [N,6]: x1,y1,x2,y2,conf,cls
            cols = ["xmin","ymin","xmax","ymax","confidence","class"]
            df = pd.DataFrame(arr, columns=cols)
            if "class" in df and names:
                df["name"] = df["class"].astype(int).map(lambda i: names[i] if 0 <= i < len(names) else str(i))

        if not df.empty:
            labels = df["name"].astype(str).tolist() if "name" in df.columns else []
            return {"result": ", ".join(labels), "raw": df.to_dict()}

        return {"result": "Không nhận diện được board!", "raw": df.to_dict()}

    except Exception as e:
        print("SERVER ERROR:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    # Nhớ mở firewall cho cổng 8000 nếu gọi từ điện thoại
    uvicorn.run(app, host="0.0.0.0", port=8000)
