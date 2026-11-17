import os
from PIL import Image, ImageDraw, ImageFont

base_dir = r"C:\Users\ravi\.gemini\antigravity\scratch\anjali_portfolio"

# --- 1. GENERATE BRAND LOCKUP (Section 2.1) ---
lockup_w, lockup_h = 1000, 320
lockup = Image.new("RGBA", (lockup_w, lockup_h), (255, 255, 255, 255))
ldraw = ImageDraw.Draw(lockup)

# Draw AR Logo on Left
logo_box = [(40, 35), (280, 275)]
radius = 45
ldraw.rounded_rectangle(logo_box, radius=radius, fill=(19, 39, 66, 255))

try:
    font_logo = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 95)
    font_name = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
    font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 22)
except:
    font_logo = font_name = font_sub = font_tag = ImageFont.load_default()

# Logo Text
cyan = (0, 194, 203, 255)
ldraw.text((80, 100), "AR", fill=cyan, font=font_logo)

# Pin/Circuit Node
node_c = (235, 95)
ldraw.ellipse([(node_c[0]-16, node_c[1]-16), (node_c[0]+16, node_c[1]+16)], fill=(235, 175, 75, 255))
ldraw.line([(225, 105), (255, 155)], fill=cyan, width=10)

# Right Side Text
ldraw.text((330, 75), "ANJALI RATHORE", fill=(19, 39, 66, 255), font=font_name)
ldraw.text((330, 145), "AI   •   DATA   •   TECHNOLOGY", fill=cyan, font=font_sub)
ldraw.text((330, 195), "Learning with data. Building with code.", fill=(83, 98, 115, 255), font=font_tag)

lockup_path = os.path.join(base_dir, "ar_brand_lockup.png")
lockup.save(lockup_path)
print("Saved Brand Lockup:", lockup_path)


# --- 2. GENERATE SOCIAL MEDIA POST TEMPLATE (Section 2.5) ---
post_size = (900, 900)
post = Image.new("RGBA", post_size, (244, 247, 250, 255)) # Cloud white background #F4F7FA
pdraw = ImageDraw.Draw(post)

# Outer Card Frame with rounded border
card_box = [(40, 40), (860, 860)]
pdraw.rounded_rectangle(card_box, radius=36, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=3)

# Top Bar Pill
pill_box = [(70, 70), (830, 135)]
pdraw.rounded_rectangle(pill_box, radius=16, fill=(19, 39, 66, 255))

try:
    font_pill = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18)
    font_h1 = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 52)
    font_body = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
    font_body_b = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
    font_foot = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
except:
    font_pill = font_h1 = font_body = font_body_b = font_foot = ImageFont.load_default()

pdraw.text((95, 90), "LEARNING LOG  /  TECH NOTES", fill=(255, 255, 255, 255), font=font_pill)

# Headline
pdraw.text((80, 200), "ONE IDEA.", fill=(19, 39, 66, 255), font=font_h1)
pdraw.text((80, 265), "CLEARLY EXPLAINED.", fill=cyan, font=font_h1)

# Gold Accent Line
pdraw.line([(80, 345), (250, 345)], fill=(230, 184, 92, 255), width=8)

# What I learned body
pdraw.text((80, 395), "What I learned", fill=(19, 39, 66, 255), font=font_body_b)
pdraw.text((105, 455), "• The key concept", fill=(83, 98, 115, 255), font=font_body)
pdraw.text((105, 510), "• A practical example", fill=(83, 98, 115, 255), font=font_body)
pdraw.text((105, 565), "• One useful takeaway", fill=(83, 98, 115, 255), font=font_body)

# Bottom Teal Accent Line
pdraw.line([(80, 755), (820, 755)], fill=cyan, width=4)

# Footer
pdraw.text((80, 785), "ANJALI RATHORE", fill=(19, 39, 66, 255), font=font_foot)
pdraw.text((360, 785), "|    DATA  •  TECHNOLOGY", fill=(83, 98, 115, 255), font=font_foot)

post_path = os.path.join(base_dir, "anjali_post_template.png")
post.save(post_path)
print("Saved Post Template:", post_path)
