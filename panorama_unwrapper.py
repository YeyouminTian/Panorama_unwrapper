import cv2
import numpy as np
import os

MAX_SIZE = 16000  # 设置一个与perspective_view_generator.py相同的最大尺寸

def resize_image(image, max_size):
    h, w = image.shape[:2]
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        new_size = (int(w * scale), int(h * scale))
        return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return image

def equirectangular_to_cubemap(equirectangular, face_size):
    equirectangular = resize_image(equirectangular, MAX_SIZE)
    face_size = min(face_size, MAX_SIZE // 2)  # 确保立方体面不会太大
    
    faces = []
    h, w = equirectangular.shape[:2]
    
    # 预计算坐标网格
    x, y = np.meshgrid(np.linspace(-1, 1, face_size), np.linspace(-1, 1, face_size))

    for i in range(6):
        if i == 0:   # 左
            X, Y, Z = 1, -y, -x
        elif i == 1: # 后
            X, Y, Z = -x, -y, -1
        elif i == 2: # 右
            X, Y, Z = -1, -y, x
        elif i == 3: # 前
            X, Y, Z = x, -y, 1
        elif i == 4: # 上
            X, Y, Z = x, 1, y
        elif i == 5: # 下
            X, Y, Z = x, -1, -y
        
        theta = np.arctan2(Z, X)
        phi = np.arctan2(Y, np.sqrt(X**2 + Z**2))
        
        uf = (w - 1) * (0.5 + theta / (2 * np.pi))
        vf = (h - 1) * (0.5 - phi / np.pi)
        
        ui = np.clip(uf.astype(int), 0, w-1)
        vi = np.clip(vf.astype(int), 0, h-1)
        
        face = equirectangular[vi, ui]
        faces.append(face)
    
    return faces

def process_image(input_path, output_dir, scale_factor=2):
    # 读取全景图
    equirectangular = cv2.imread(input_path)
    
    if equirectangular is None:
        print(f"无法读取图像: {input_path}")
        return
    
    # 设置立方体每个面的大小，确保是整数
    face_size = min(int(min(equirectangular.shape[:2]) // 2 * scale_factor), MAX_SIZE // 2)
    
    # 生成六个面
    faces = equirectangular_to_cubemap(equirectangular, face_size)
    
    # 保存六个面
    face_names = ['left', 'back', 'right', 'front', 'top', 'bottom']
    base_name = os.path.splitext(os.path.basename(input_path))[0]  # 获取文件名（不含扩展名）
    for i, face in enumerate(faces):
        # 对每个面进行水平镜像
        mirrored_face = cv2.flip(face, 1)
        output_filename = f'{base_name}_{face_names[i]}.jpg'
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, mirrored_face)
        print(f"已保存镜像后的面: {output_path}")

# 主函数保持不变
