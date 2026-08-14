"""
二维码生成工具
"""

from pathlib import Path
import qrcode


class QRCodeUtils:
    """
    二维码工具类
    """

    @staticmethod
    async def generate_qrcode(content: str, save_path: Path) -> Path:
        """
        根据字符串生成二维码图片

        参数：
            content: 要编码的内容（通常是下载链接）
            save_path: 图片保存路径

        返回：
            生成后的图片路径
        """

        # 创建二维码对象
        qr = qrcode.QRCode(
            version=1,          # 自动控制二维码尺寸
            box_size=10,        # 每个小格子的像素大小
            border=4            # 外边框宽度
        )

        # 添加内容
        qr.add_data(content)

        # 生成二维码
        qr.make(fit=True)

        # 创建图片
        img = qr.make_image(fill_color="black", back_color="white")

        # 确保目录存在
        await save_path.parent.mkdir(parents=True, exist_ok=True)

        # 保存图片
        await img.save(save_path)

        return save_path