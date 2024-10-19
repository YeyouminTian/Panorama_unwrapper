import os
import argparse
from panorama_unwrapper import process_image

def main():
    parser = argparse.ArgumentParser(description='处理全景图并生成立方体贴图')
    parser.add_argument('--input_dir', default=r'img\panorama', help='输入图片所在的文件夹路径')
    parser.add_argument('--output_dir', default=r'img\six_face', help='输出图片的保存文件夹路径')
    parser.add_argument('--scale', type=int, default=2, help='输出图片的缩放因子 (默认: 2)')
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 获取输入文件夹中的所有jpg文件
    input_files = [f for f in os.listdir(args.input_dir) if f.lower().endswith('.jpg')]
    
    if not input_files:
        print(f"在 {args.input_dir} 中没有找到jpg文件")
        return
    
    # 处理每个文件
    for filename in input_files:
        input_path = os.path.join(args.input_dir, filename)
        process_image(input_path, args.output_dir, args.scale)

if __name__ == '__main__':
    main()
