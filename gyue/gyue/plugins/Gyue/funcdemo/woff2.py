from fontTools.ttLib import TTFont

def convert_woff2_to_ttf(woff2_path, ttf_output_path):
    """
    将 woff2 字体文件转换为 ttf 格式。
    :param woff2_path: 输入的 woff2 文件路径
    :param ttf_output_path: 转换后的 ttf 文件路径
    """
    font = TTFont(woff2_path)
    font.save(ttf_output_path)
    print(f"字体已从 woff2 转换为 ttf：{ttf_output_path}")

# 示例用法
woff2_file = r"D:\Bot\GyueBot\Data\extensions\ygoc\src\assets\yugioh-card\custom-font\custom1.woff"  # 输入的 woff2 文件路径
ttf_file = r"D:\Bot\GyueBot\gyue\gyue\gyue\plugins\Gyue\funcdemo\font.ttf"     # 输出的 ttf 文件路径
convert_woff2_to_ttf(woff2_file, ttf_file)