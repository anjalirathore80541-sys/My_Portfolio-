from PIL import Image, ImageDraw, ImageFont
import math

dest_dir = r"C:\Users\ravi\.gemini\antigravity\scratch\anjali_portfolio"

# --- 1. GENERATE AR LOGO ---
logo_size = (500, 500)
logo = Image.new("RGBA", logo_size, (0, 0, 0, 0))
draw = ImageDraw.Draw(logo)

# Rounded rectangle background
bg_color = (19, 39, 66, 255) # Deep navy #132742
radius = 80
draw.rounded_rectangle([(20, 20), (480, 480)], radius=radius, fill=bg_color)

# Draw AR text
try:
    font_logo = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 150)
except:
    font_logo = ImageFont.load_default()

cyan_color = (0, 194, 203, 255) # #00C2CB
draw.text((85, 160), "AR", fill=cyan_color, font=font_logo)

# Circuit / node line element on top right
gold_color = (235, 175, 75, 255) # #EBAF4B
node_center = (400, 130)
node_radius = 26
draw.ellipse(
    [(node_center[0] - node_radius, node_center[1] - node_radius),
     (node_center[0] + node_radius, node_center[1] + node_radius)],
    fill=gold_color
)

# Line connecting down to circuit
line_start = (385, 150)
line_end = (435, 230)
draw.line([line_start, line_end], fill=cyan_color, width=16)

logo.save(dest_dir + r"\ar_logo.png")
print("Saved AR Logo!")

# --- 2. GENERATE BRAND BANNER ---
banner_size = (1200, 300)
banner = Image.new("RGBA", banner_size, (13, 33, 55, 255)) # Deep navy
bdraw = ImageDraw.Draw(banner)

try:
    font_name = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 46)
    font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 22)
    font_skills = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 15)
except:
    font_name = font_tag = font_skills = ImageFont.load_default()

# Text on left
bdraw.text((70, 75), "ANJALI RATHORE", fill=(255, 255, 255, 255), font=font_name)
bdraw.text((70, 140), "Learning with data. Building with code.", fill=(0, 194, 203, 255), font=font_tag)
bdraw.text((70, 205), "AI & DATA SCIENCE   |   PYTHON   |   DATA ANALYSIS   |   WEB DEVELOPMENT", fill=(203, 213, 225, 255), font=font_skills)

# Network Nodes on right side
nodes = [
    (920, 60),
    (1010, 85),
    (935, 140),
    (880, 225),
    (1005, 260),
    (1070, 170),
    (1085, 275)
]

connections = [
    (0, 2), (1, 2), (1, 5), (2, 3), (2, 4), (3, 4), (5, 6)
]

# Draw network connection lines
for p1_idx, p2_idx in connections:
    p1 = nodes[p1_idx]
    p2 = nodes[p2_idx]
    bdraw.line([p1, p2], fill=(47, 95, 130, 255), width=3)

# Draw network node circles
for pt in nodes:
    r = 11
    bdraw.ellipse([(pt[0]-r, pt[1]-r), (pt[0]+r, pt[1]+r)], fill=(0, 194, 203, 255))

banner.save(dest_dir + r"\anjali_banner.png")
print("Saved Brand Banner!")
