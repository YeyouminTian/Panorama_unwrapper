import cv2
import numpy as np
import os

def equirectangular_to_perspective(img, fov_h, fov_v, heading, pitch, out_size):
    """
    将等距柱状投影图像转换为透视图，减少畸变但保持尺寸和视角
    :param img: 输入的等距柱状投影图像
    :param fov_h: 水平视场角（度）
    :param fov_v: 垂直视场角（度）
    :param heading: 水平旋转角度（度）
    :param pitch: 垂直俯仰角度（度）
    :param out_size: 输出图像的尺寸 (宽度, 高度)
    :return: 透视图
    """
    height, width = img.shape[:2]
    
    # 使用指定的输出尺寸
    out_w, out_h = out_size
    
    # 创建网格
    x = np.linspace(-np.tan(np.radians(fov_h/2)), np.tan(np.radians(fov_h/2)), out_w)
    y = np.linspace(-np.tan(np.radians(fov_v/2)), np.tan(np.radians(fov_v/2)), out_h)
    x_grid, y_grid = np.meshgrid(x, y)

    # 计算三维单位向量
    z = np.ones_like(x_grid)
    norm = np.sqrt(x_grid**2 + y_grid**2 + z**2)
    x = x_grid / norm
    y = y_grid / norm
    z = z / norm

    # 应用旋转
    heading_rad = np.radians(heading)
    pitch_rad = np.radians(pitch)
    
    # 绕y轴旋转（heading）
    x_rot = x * np.cos(heading_rad) + z * np.sin(heading_rad)
    y_rot = y
    z_rot = -x * np.sin(heading_rad) + z * np.cos(heading_rad)
    
    # 绕x轴旋转（pitch）
    x = x_rot
    y = y_rot * np.cos(pitch_rad) - z_rot * np.sin(pitch_rad)
    z = y_rot * np.sin(pitch_rad) + z_rot * np.cos(pitch_rad)

    # 将三维坐标转换为等距柱状投影坐标
    lon = np.arctan2(x, z)
    lat = np.arcsin(y)
    
    x_eq = (lon / (2 * np.pi) + 0.5) * width
    y_eq = (lat / np.pi + 0.5) * height

    # 使用双线性插值进行重采样
    perspective = cv2.remap(img, x_eq.astype(np.float32), y_eq.astype(np.float32), cv2.INTER_LINEAR)

    return perspective

def generate_perspective_views(input_path, output_dir, fov_h=100, fov_v=55, out_size=(1920, 1080)):
    # 读取全景图
    equirectangular = cv2.imread(input_path)
    
    if equirectangular is None:
        print(f"无法读取图像: {input_path}")
        return
    
    print(f"处理图像: {input_path}")
    print(f"原始图像大小: {equirectangular.shape}")
    
    # 获取基本文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    # 生成各个视图
    right_view = equirectangular_to_perspective(equirectangular, fov_h, fov_v, 0, 0, out_size)
    left_view = equirectangular_to_perspective(equirectangular, fov_h, fov_v, 180, 0, out_size)
    back_view = equirectangular_to_perspective(equirectangular, fov_h, fov_v, -90, 0, out_size)
    front_view = equirectangular_to_perspective(equirectangular, fov_h, fov_v, 90, 0, out_size)
    
    # 保存各个视图到对应的子文件夹
    for view, name in [(left_view, 'left'), (right_view, 'right'), (front_view, 'front'), (back_view, 'back')]:
        if view is not None and view.size > 0 and view.max() > 0:  # 确保图像不是全黑的
            # 创建对应的子文件夹
            sub_dir = os.path.join(output_dir, name)
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)
            
            output_path = os.path.join(sub_dir, f'{base_name}_{name}_view.jpg')
            cv2.imwrite(output_path, view)
            print(f"已保存{name}视图: {output_path}")
        else:
            print(f"警告: {name}视图生成失败或全黑")
