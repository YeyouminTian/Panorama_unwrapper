import os
from perspective_view_generator import generate_perspective_views

def process_folder(input_folder, output_folder, fov_h=100, fov_v=55, out_size=(1920, 1080)):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有图片文件
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = [f for f in os.listdir(input_folder) if os.path.splitext(f.lower())[1] in image_extensions]

    # 处理每个图片文件
    for image_file in image_files:
        input_path = os.path.join(input_folder, image_file)
        generate_perspective_views(input_path, output_folder, fov_h, fov_v, out_size)

    print(f"所有图片处理完成。输出文件夹: {output_folder}")

if __name__ == "__main__":
    # 设置输入和输出文件夹
    input_folder = r"img\panorama"
    output_folder = r"img\perspective"

    # 设置参数（可以根据需要调整）
    fov_h = 100
    fov_v = 55
    out_size = (1920, 1080)

    # 处理文件夹中的所有图片
    process_folder(input_folder, output_folder, fov_h, fov_v, out_size)
