import sys

import torch
from PIL import Image

# Đường dẫn model và ảnh test
MODEL_PATH = './best.pt'  # Đặt đúng tên file model YOLOv7
IMG_PATH = './test.png'   # Đặt đúng tên file ảnh test

if len(sys.argv) > 1:
    IMG_PATH = sys.argv[1]

# Load model YOLOv7
model = torch.hub.load('WongKinYiu/yolov7', 'custom', MODEL_PATH, force_reload=True)

# Load ảnh test
image = Image.open(IMG_PATH).convert('RGB')

# Chạy detect
results = model(image)
df = results.pandas().xyxy[0]
print('Detection dataframe:')
print(df)
if not df.empty:
    print('Detected labels:', df['name'].tolist() if 'name' in df.columns else df['class'].tolist())
else:
    print('Không detect được object nào!')
