import os
import zipfile
from PIL import Image

output_docx = r"C:\Users\ravi\.gemini\antigravity\scratch\anjali_portfolio\Anjali_Rathore_Assignment_2.docx"
base_dir = r"C:\Users\ravi\.gemini\antigravity\scratch\anjali_portfolio"

# Source images
img_logo = os.path.join(base_dir, "ar_logo.png")
img_banner = os.path.join(base_dir, "anjali_banner.png")
img_portfolio = os.path.join(base_dir, "portfolio_preview.png")
img_avatar = os.path.join(base_dir, "anjali_avatar_circle.png")
img_linkedin = os.path.join(base_dir, "screenshot_linkedin.png")

# Calculate EMU dimensions preserving aspect ratio (max width = 6.0 inches = 5486400 EMUs)
def get_emu_dimensions(img_path, max_width_in=6.0, max_height_in=6.5):
    with Image.open(img_path) as im:
        w, h = im.size
    aspect = h / w
    target_w_in = min(max_width_in, max_height_in / aspect)
    target_h_in = target_w_in * aspect
    return int(target_w_in * 914400), int(target_h_in * 914400)

emu_logo = get_emu_dimensions(img_logo, max_width_in=2.5, max_height_in=2.5)
emu_banner = get_emu_dimensions(img_banner, max_width_in=6.2, max_height_in=2.0)
emu_portfolio = get_emu_dimensions(img_portfolio, max_width_in=6.0, max_height_in=5.5)
emu_avatar = get_emu_dimensions(img_avatar, max_width_in=2.4, max_height_in=2.4)
emu_linkedin = get_emu_dimensions(img_linkedin, max_width_in=6.2, max_height_in=3.6)

print("EMUs calculated successfully!")
