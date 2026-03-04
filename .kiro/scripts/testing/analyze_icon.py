"""
分析 icon.png 图像文件
"""
import base64
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ICON_PATH = PROJECT_ROOT / "icon.png"

def analyze_icon():
    """分析 icon.png 文件"""
    print("=" * 60)
    print("Icon.png 分析")
    print("=" * 60)
    
    if not ICON_PATH.exists():
        print(f"\n❌ 文件不存在: {ICON_PATH}")
        return
    
    # 读取文件
    with open(ICON_PATH, 'rb') as f:
        data = f.read()
    
    # 基本信息
    print(f"\n📁 文件路径: {ICON_PATH}")
    print(f"📊 文件大小: {len(data)} 字节 ({len(data)/1024:.2f} KB)")
    
    # PNG 文件头检查
    png_signature = b'\x89PNG\r\n\x1a\n'
    if data[:8] == png_signature:
        print(f"✅ PNG 文件签名: 有效")
    else:
        print(f"❌ PNG 文件签名: 无效")
        return
    
    # 读取 IHDR 块（图像头）
    # PNG 结构: 8字节签名 + 块(长度4字节 + 类型4字节 + 数据 + CRC4字节)
    ihdr_length = int.from_bytes(data[8:12], 'big')
    ihdr_type = data[12:16].decode('ascii')
    
    if ihdr_type == 'IHDR':
        ihdr_data = data[16:16+ihdr_length]
        width = int.from_bytes(ihdr_data[0:4], 'big')
        height = int.from_bytes(ihdr_data[4:8], 'big')
        bit_depth = ihdr_data[8]
        color_type = ihdr_data[9]
        
        color_type_names = {
            0: "灰度",
            2: "RGB",
            3: "索引色",
            4: "灰度+Alpha",
            6: "RGBA"
        }
        
        print(f"\n🖼️  图像信息:")
        print(f"   宽度: {width} 像素")
        print(f"   高度: {height} 像素")
        print(f"   位深度: {bit_depth} 位")
        print(f"   颜色类型: {color_type_names.get(color_type, '未知')} ({color_type})")
    
    # Base64 编码
    base64_data = base64.b64encode(data).decode('utf-8')
    print(f"\n🔤 Base64 编码:")
    print(f"   长度: {len(base64_data)} 字符")
    print(f"   前50字符: {base64_data[:50]}...")
    
    # 用途说明
    print(f"\n📝 用途:")
    print(f"   这是 Godot 项目的默认图标文件")
    print(f"   用于显示在编辑器和导出的应用程序中")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    analyze_icon()
