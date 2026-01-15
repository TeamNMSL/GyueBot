from psd_tools import PSDImage
from PIL import Image, ImageDraw, ImageFont




def exportCardImg(psdpath,layervis,outputpath,img):
    psd=PSDImage.open(psdpath) #打开
    for layer in psd:
        # layer.visible=getshowlayerStat(layervis,layer.name)
        print(f"{layer.name}")
        if layer.is_group():
            for llayer in layer:
                # llayer.visible=getshowlayerStat(layervis,llayer.name)
                print(f"{layer.name}.{llayer.name}")




def getshowlayerStat(layervisInt,layername):
    """
     
    """
    return False
def export_psd_with_text_rendering(psd_path, output_path, font_path=None):
    """
    将 PSD 文件导出为图片，并支持文字图层的字体渲染。

    :param psd_path: PSD 文件的路径
    :param output_path: 导出的图片路径
    :param font_path: 字体文件路径（用于渲染文字图层）
    """
    # 加载 PSD 文件
    psd = PSDImage.open(psd_path)

    # 将 PSD 文件合成为单张图片
    composite_image = psd.composite()

    # 如果不需要字体渲染，直接保存图片
    if not font_path:
        composite_image.save(output_path)
        print(f"PSD 文件已导出为图片：{output_path}")
        return

    # 如果需要渲染文字，使用 Pillow 加载图片
    image = composite_image.convert("RGB")
    draw = ImageDraw.Draw(image)

    # 遍历 PSD 图层，找到文字图层
    for layer in psd:
        if layer.kind=="type":
            # 获取文字和位置信息
            text = layer.text
            left, top, right, bottom = layer.bbox

            # 设置字体
            try:
                font = ImageFont.truetype(font_path, size=int(layer.fonts[0].size))
            except Exception as e:
                print(f"字体加载失败：{e}")
                font = ImageFont.load_default()

            # 在图片上绘制文字
            draw.text((left, top), text, font=font, fill="black")

    # 保存最终的图片
    image.save(output_path)
    print(f"PSD 文件已导出为图片，并渲染文字：{output_path}")


# 示例用法
psd_file = "D:/Bot/GyueBot/Data/img/yugioh/card.psd"  # PSD 文件路径
output_file = "D:/Bot/GyueBot/Data/img/yugioh/output_image.jpg"  # 导出的图片路径
font_file = "path/to/font.ttf"  # 字体文件路径

exportCardImg(psd_file,"","","")