import os
import zipfile
import html
from PIL import Image

base_dir = r"C:\Users\ravi\.gemini\antigravity\scratch\anjali_portfolio"
out_docx = os.path.join(base_dir, "Anjali_Rathore_Assignment_2.docx")

img_files = {
    "rIdImgLogo": ("ar_logo.png", "image/png"),
    "rIdImgBanner": ("anjali_banner.png", "image/png"),
    "rIdImgPortfolio": ("portfolio_preview.png", "image/png"),
    "rIdImgAvatar": ("anjali_avatar_circle.png", "image/png"),
    "rIdImgLinkedIn": ("screenshot_linkedin.png", "image/png"),
}

# EMU helper
def get_emu(filename, max_w_in=6.0, max_h_in=6.0):
    filepath = os.path.join(base_dir, filename)
    with Image.open(filepath) as im:
        w, h = im.size
    aspect = h / w
    target_w_in = min(max_w_in, max_h_in / aspect)
    target_h_in = target_w_in * aspect
    return int(target_w_in * 914400), int(target_h_in * 914400)

emu_map = {
    "rIdImgLogo": get_emu("ar_logo.png", 2.6, 2.6),
    "rIdImgBanner": get_emu("anjali_banner.png", 6.2, 1.8),
    "rIdImgPortfolio": get_emu("portfolio_preview.png", 6.0, 5.4),
    "rIdImgAvatar": get_emu("anjali_avatar_circle.png", 2.4, 2.4),
    "rIdImgLinkedIn": get_emu("screenshot_linkedin.png", 6.2, 3.4),
}

class DocxBuilder:
    def __init__(self):
        self.paragraphs = []
        self.doc_pr_id = 1

    def p(self, text="", bold=False, italic=False, size=22, align="left", space_before=60, space_after=60, color=None):
        safe_text = html.escape(text)
        jc = f'<w:jc w:val="{align}"/>' if align != "left" else ''
        clr = f'<w:color w:val="{color}"/>' if color else ''
        b = '<w:b/>' if bold else ''
        i = '<w:i/>' if italic else ''
        xml = f'''<w:p>
  <w:pPr>
    {jc}
    <w:spacing w:before="{space_before}" w:after="{space_after}" w:line="276" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      {b}{i}{clr}
      <w:sz w:val="{size}"/>
    </w:rPr>
    <w:t xml:space="preserve">{safe_text}</w:t>
  </w:r>
</w:p>'''
        self.paragraphs.append(xml)

    def heading(self, text, level=1):
        if level == 1:
            self.p(text, bold=True, size=28, space_before=240, space_after=100, color="0F172A")
        elif level == 2:
            self.p(text, bold=True, size=24, space_before=180, space_after=80, color="1E293B")
        elif level == 3:
            self.p(text, bold=True, size=22, space_before=140, space_after=60, color="334155")

    def image(self, rel_id, align="center"):
        cx, cy = emu_map[rel_id]
        doc_id = self.doc_pr_id
        self.doc_pr_id += 1
        jc = f'<w:jc w:val="{align}"/>'
        xml = f'''<w:p>
  <w:pPr>
    {jc}
    <w:spacing w:before="120" w:after="120"/>
  </w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_id}" name="Picture {doc_id}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="{doc_id}" name="Picture {doc_id}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''
        self.paragraphs.append(xml)

    def table(self, headers, rows, col_widths=None):
        if not col_widths:
            w_each = 9000 // len(headers)
            col_widths = [w_each] * len(headers)

        xml = ['<w:tbl>',
               '<w:tblPr>',
               '  <w:tblW w:w="9000" w:type="dxa"/>',
               '  <w:jc w:val="center"/>',
               '  <w:tblBorders>',
               '    <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>',
               '    <w:left w:val="none"/>',
               '    <w:bottom w:val="single" w:sz="8" w:space="0" w:color="94A3B8"/>',
               '    <w:right w:val="none"/>',
               '    <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>',
               '    <w:insideV w:val="none"/>',
               '  </w:tblBorders>',
               '</w:tblPr>']

        # Header Row
        xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
        for idx, h_text in enumerate(headers):
            w = col_widths[idx]
            xml.append(f'''<w:tc>
  <w:tcPr>
    <w:tcW w:w="{w}" w:type="dxa"/>
    <w:shd w:val="clear" w:color="auto" w:fill="0F172A"/>
    <w:tcMar><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>
  </w:tcPr>
  <w:p>
    <w:pPr><w:spacing w:before="60" w:after="60"/></w:pPr>
    <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/></w:rPr><w:t>{html.escape(h_text)}</w:t></w:r>
  </w:p>
</w:tc>''')
        xml.append('</w:tr>')

        # Data Rows
        for r_idx, row in enumerate(rows):
            bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            xml.append('<w:tr>')
            for idx, c_text in enumerate(row):
                w = col_widths[idx]
                xml.append(f'''<w:tc>
  <w:tcPr>
    <w:tcW w:w="{w}" w:type="dxa"/>
    <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
    <w:tcMar><w:top w:w="100" w:type="dxa"/><w:bottom w:w="100" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>
  </w:tcPr>
  <w:p>
    <w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>
    <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="20"/></w:rPr><w:t>{html.escape(c_text)}</w:t></w:r>
  </w:p>
</w:tc>''')
            xml.append('</w:tr>')

        xml.append('</w:tbl>')
        self.paragraphs.append('\n'.join(xml))

    def build_xml(self):
        body_content = '\n'.join(self.paragraphs)
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

doc = DocxBuilder()

# HEADER
doc.p("K.R. MANGALAM UNIVERSITY", bold=True, size=32, align="center", space_before=100, space_after=40, color="0F172A")
doc.p("GURUGRAM, HARYANA", bold=True, size=24, align="center", space_before=20, space_after=140, color="475569")
doc.p("ASSESSMENT – 2", bold=True, size=28, align="center", space_before=40, space_after=40, color="0284C7")
doc.p("AI-BASED VISUAL BRANDING, DIGITAL PRESENCE, AND ENGAGEMENT ANALYTICS", bold=True, size=24, align="center", space_before=20, space_after=40, color="0F172A")
doc.p("Building Your Personal Digital Brand with AI Tools (VAC-II)", italic=True, size=22, align="center", space_before=20, space_after=180, color="334155")

# Student Details Table
doc.table(
    ["Field", "Details"],
    [
        ["Name", "Anjali Rathore"],
        ["Roll Number", "2501201025"],
        ["Programme & School", "BCA – School of Engineering and Technology"],
        ["Faculty Name", "Dr. Aarti"],
        ["Maximum Marks", "5"]
    ],
    col_widths=[3200, 5800]
)

doc.p("Submitted as part of the internal assessment", italic=True, size=20, align="center", space_before=120, space_after=200, color="64748B")

# Assignment Overview
doc.heading("Assignment Overview", level=2)
doc.p("This assignment presents a personal digital branding plan using AI-assisted design and content tools. It covers visual identity, a personal introduction video, a portfolio website, LinkedIn profile improvement, a five-day content calendar, analytics metrics, engagement strategies, and a short branding campaign.")
doc.p("Personal brand direction: A BCA student interested in AI, data science, Python programming, web development, and digital design.", italic=True, bold=True, color="0284C7")

# Section 1
doc.heading("1. Personal Logo and Brand Banner", level=2)
doc.p("Personal Logo:", bold=True)
doc.image("rIdImgLogo", align="left")
doc.p("LinkedIn / Portfolio Banner:", bold=True)
doc.image("rIdImgBanner", align="center")
doc.p('My personal brand will use the name “Anjali Rathore” with a clean, modern, technology-focused identity. The logo uses the initials “AR” in a simple geometric style. A small circuit-line or digital-node element is included to represent technology, AI, and problem-solving.')
doc.p('Banner concept: “Anjali Rathore | BCA – AI & Data Science | Python • Web Development • AI”')
doc.p('Tool: Canva AI. I used Canva’s logo and banner design features, reviewed the generated options, and refined the design so it looks original, modern, and professional.')

# Section 2
doc.heading("2. Visual Identity: Logo, Colours, and Typography", level=2)
doc.table(
    ["Element", "Selection", "Reason"],
    [
        ["Logo", "AR monogram with a subtle digital/circuit element", "Simple, memorable, and technology-oriented."],
        ["Primary colour", "Midnight Navy (#0F172A)", "Communicates trust, depth, and professionalism."],
        ["Secondary colour", "Cyan blue (#06B6D4)", "Suggests innovation, creativity, and modern technology."],
        ["Accent colour", "Crisp White (#FFFFFF)", "Keeps the design clean and readable."],
        ["Heading font", "Poppins SemiBold / Montserrat", "Modern, geometric, and clear for titles."],
        ["Body font", "Calibri / Open Sans", "Highly readable for longer descriptive text."]
    ],
    col_widths=[2200, 3600, 3200]
)

# Section 3
doc.heading("3. 60-Second AI-Generated Personal Introduction Video", level=2)
doc.p("The video will introduce me, my academic background, my technical interests, and the skills I am developing. It should be approximately 60 seconds long and use clear visuals, readable text, and background music at a low volume.")
doc.heading("Suggested 60-second video script", level=3)
doc.p("0–10 seconds: Hello, I’m Anjali Rathore, a BCA student at K.R. Mangalam University, interested in technology and innovation.")
doc.p("10–25 seconds: I am exploring Artificial Intelligence and Data Science, and building my programming foundation with Python.")
doc.p("25–40 seconds: I also enjoy web development and digital design. I like turning ideas into useful, simple, and user-friendly digital solutions.")
doc.p("40–52 seconds: I continuously work on improving my problem-solving, technical, and creative skills through learning and projects.")
doc.p("52–60 seconds: My goal is to grow as a technology professional and contribute to meaningful projects. Thank you for watching.")

doc.heading("What to do in the video (step-by-step)", level=3)
doc.p("1. Write and practise the script above. Keep the final video close to 60 seconds.")
doc.p("2. Create the video using Canva, Pictory, Lumen5, or Animoto. Select a clean professional template in the same midnight-navy and cyan colour theme.")
doc.p("3. Add an opening title with your name, “Anjali Rathore”, and “BCA – AI & Data Science”.")
doc.p("4. Add short scenes or visuals related to coding, Python, AI/data, web development, and learning. Use only visuals that support what you are saying.")
doc.p("5. Record your own voice reading the script, or use a suitable AI voice. Add captions so the video is understandable without sound.")
doc.p("6. End with your name and a short line such as “Learning • Building • Growing”. Check spelling, audio, timing, and video quality.")
doc.p("7. Export the video as MP4. Upload it to GitHub repository or portfolio link:")
doc.p("GitHub / Video Link: https://github.com/anjalirathore80541-sys/personal-branding-vac2", bold=True, color="0284C7")
doc.p("Repository name: personal-branding-vac2", italic=True)

# Section 4
doc.heading("4. Portfolio Website Using Carrd or Notion", level=2)
doc.p("I have created a responsive one-page portfolio website. The website acts as a central place to show my introduction, skills, projects, learning progress, and contact details.")
doc.p("• Home: Name, professional photo avatar, and short introduction.")
doc.p("• About: BCA – AI & Data Science student at K.R. Mangalam University.")
doc.p("• Skills: Python, Data Analysis, AI Fundamentals, Web Development, SQL, and UI/UX Design.")
doc.p("• Projects: Data & Analytics EDA project, Responsive Web Platform, and AI Machine Learning models.")
doc.p("• Contact & Professional Profiles: LinkedIn profile link and GitHub repository links.")
doc.p("Portfolio website link: Open Anjali Rathore Portfolio Website (Open the accompanying HTML file: Anjali_Rathore_Portfolio_Website.html)", bold=True, color="0284C7")
doc.p("GitHub Profile: https://github.com/anjalirathore80541-sys", bold=True)
doc.p("LinkedIn Profile: https://www.linkedin.com/in/anjali-rathore-a9436930b/", bold=True)

# Section 5
doc.heading("5. LinkedIn Profile Optimization", level=2)
doc.p("Profile URL: https://www.linkedin.com/in/anjali-rathore-a9436930b/", bold=True, color="0284C7")
doc.p("Suggested headline:", bold=True)
doc.p("BCA – AI & Data Science Student | Python | Web Development | Exploring AI, Data Analytics & Technology", italic=True)
doc.p("Suggested About section:", bold=True)
doc.p("I am a BCA student with an interest in Artificial Intelligence, Data Science, and technology. I am developing my programming skills with Python and exploring web development and digital design. I enjoy learning new tools, solving problems, and building practical projects. I aim to keep improving my technical and analytical abilities through coursework, projects, and hands-on experience.")
doc.p("Featured section: Added Portfolio website, GitHub profile (https://github.com/anjalirathore80541-sys), best project repositories, and the 60-second introduction video.", bold=True)
doc.p("Featured skills: Python, Problem Solving, Web Development, HTML, CSS, JavaScript, Data Analysis, and Figma (include only skills that I can demonstrate).")

# Section 6
doc.heading("6. Five-Day AI-Assisted LinkedIn Content Calendar", level=2)
doc.table(
    ["Day", "Post topic", "Content idea", "Purpose"],
    [
        ["Day 1", "My learning journey", "Introduce myself, my BCA course, and my interest in AI and Data Science.", "Build awareness."],
        ["Day 2", "Python learning", "Share one Python concept learned, with a small example or code screenshot.", "Show learning progress."],
        ["Day 3", "Web development", "Share a small website/UI component or project screenshot and explain how it works.", "Demonstrate practical skills."],
        ["Day 4", "AI and Data Science", "Share a simple insight about an AI/data science concept and why it is useful.", "Encourage discussion."],
        ["Day 5", "Weekly reflection", "Summarize what I learned, what I built, and my next learning goal.", "Encourage engagement."]
    ],
    col_widths=[1400, 2400, 3600, 1600]
)
doc.p("AI assistance: Use ChatGPT to brainstorm post ideas and improve clarity, then edit every post in my own voice. Use Canva to create consistent post graphics. Verify all technical facts before publishing.")

# Section 7
doc.heading("7. Four Key Metrics in LinkedIn Analytics / Google Analytics", level=2)
doc.table(
    ["Metric", "Meaning", "Why it matters"],
    [
        ["Impressions", "Number of times a post is displayed.", "Shows the reach and visibility of content."],
        ["Engagement rate", "Engagement in relation to the content's reach or impressions, as calculated by the platform.", "Helps judge whether the audience finds the post useful or interesting."],
        ["Profile views", "Number of visits to the LinkedIn profile.", "Indicates whether content encourages people to learn more about the creator."],
        ["Link clicks", "Number of clicks on a link included in a post or profile.", "Shows whether viewers are taking action to visit a portfolio or project."]
    ],
    col_widths=[2200, 3600, 3200]
)

# Section 8
doc.heading("8. Three Strategies to Improve Online Engagement", level=2)
doc.p("1. Improve content based on performance: Review impressions and engagement rate. Create more posts on topics that receive meaningful interaction, and improve or replace topics that consistently perform poorly.")
doc.p("2. Use clear visuals and calls to action: Use consistent branded graphics, short paragraphs, and relevant questions. Invite readers to share an opinion or experience rather than asking for engagement without context.")
doc.p("3. Post consistently and review results: Follow a realistic posting schedule. Compare results across the five-day calendar and test different posting times and formats. Continue with the formats that produce stronger relevant engagement.")

# Section 9
doc.heading("9. Personal Branding Campaign: 5-Day Visibility Challenge", level=2)
doc.p("Campaign objective: Build a consistent professional presence by sharing five useful posts in five days, showing my learning journey in AI, Data Science, Python, and web development.")
doc.p("Target audience: Students, beginner developers, technology learners, and professionals interested in AI and data.")
doc.p("Campaign activities:")
doc.p("• Day 1: Publish a short introduction and explain my learning interests.")
doc.p("• Day 2: Share a Python concept or a small coding lesson.")
doc.p("• Day 3: Share a web development project or design progress.")
doc.p("• Day 4: Explain one AI or Data Science concept in simple language.")
doc.p("• Day 5: Share a weekly reflection, portfolio link, and next learning goal.")
doc.p("How success will be evaluated: Before starting, record the current profile views and recent post performance as a baseline. After the campaign, compare impressions, engagement rate, profile views, and link clicks. Also review the quality of comments and whether people visited the portfolio. The campaign will be considered useful if visibility and relevant engagement improve compared with the baseline. I will use the results to decide which topics and formats to continue.")

# Section 10
doc.heading("AI Prompts Used (Record for Submission)", level=2)
doc.p("The assignment instructions ask students to submit a brief record of AI prompts used. The following are sample prompts to use and retain while creating the actual assets:")
doc.p("1. Create three clean, professional personal logo concepts using the initials AR for a BCA student interested in AI and Data Science. Use midnight navy, cyan, and white.")
doc.p("2. Design a LinkedIn banner for Anjali Rathore, a BCA – AI & Data Science student, with a modern technology theme and the text: Python | Web Development | AI & Data Science.")
doc.p("3. Write a natural 60-second personal introduction video script for a BCA student interested in AI, Data Science, Python, and web development.")
doc.p("4. Suggest a simple one-page portfolio website structure for a student, including About, Skills, Projects, Learning, and Contact sections.")
doc.p("5. Create a five-day LinkedIn content calendar for a student sharing learning progress in Python, web development, AI, and Data Science.")

# Section 11
doc.heading("Evidence and Submission Checklist", level=2)
doc.p("☑ Personal logo and brand banner screenshots/link added.")
doc.p("☑ Colour palette and typography documented.")
doc.p("☑ 60-second introduction video created and video/GitHub link added above.")
doc.p("☑ Portfolio website URL and screenshots added.")
doc.p("☑ LinkedIn headline, About section, and featured skills updated.")
doc.p("☑ Five-day LinkedIn content calendar completed.")
doc.p("☑ Four analytics metrics and their significance explained.")
doc.p("☑ Three engagement strategies and campaign evaluation explained.")
doc.p("☑ Brief record of actual AI prompts retained and submitted.")

# Section 12
doc.heading("Conclusion", level=2)
doc.p("This assignment provides a structured plan for building a professional digital identity. By keeping the logo, banner, portfolio, LinkedIn profile, and content consistent, I can present my skills and learning journey clearly. Using analytics will help me understand audience response and improve future content. AI tools can support the process, while the final designs and content will be reviewed and personalized.")

# Section 13 - Practical Deliverables & Evidence
doc.heading("Practical Deliverables and Evidence", level=2)
doc.p("The following original branding assets have been created for this assignment and are used consistently across the portfolio and LinkedIn profile.")

doc.heading("Portfolio Website", level=3)
doc.p("A responsive one-page portfolio website has been prepared in HTML and CSS. The portfolio integrates live links to the GitHub and LinkedIn profiles.")
doc.p("Portfolio website: Open Anjali Rathore Portfolio Website (Anjali_Rathore_Portfolio_Website.html)", italic=True)
doc.p("Portfolio GitHub link: https://github.com/anjalirathore80541-sys", bold=True, color="0284C7")

doc.heading("LinkedIn Profile — Applied Information", level=3)
doc.p("LinkedIn Profile URL: https://www.linkedin.com/in/anjali-rathore-a9436930b/", bold=True, color="0284C7")
doc.p("Headline: BCA – AI & Data Science Student | Python | Web Development | Exploring AI, Data Analytics & Technology", bold=True)
doc.p("About: I am a BCA student interested in Artificial Intelligence, Data Science, and technology. I am developing my programming skills with Python and exploring web development and digital design. I enjoy learning new tools, solving problems, and building practical projects. I aim to keep improving my technical and analytical abilities through coursework, projects, and hands-on experience.")
doc.p("Featured items: portfolio website, GitHub profile, project repositories, and introduction video.")

doc.heading("Video Link", level=3)
doc.p("GitHub repository / video URL: https://github.com/anjalirathore80541-sys/personal-branding-vac2", bold=True, color="0284C7")
doc.p("Video file name: anjali_rathore_intro_60s.mp4")

# Supporting Evidence Figures (Clean - NO "Figure X ..." and NO "shown on the supplied linkedin screenshot")
doc.heading("Supporting Evidence — Portfolio Homepage Preview", level=3)
doc.image("rIdImgPortfolio", align="center")

doc.heading("Supporting Evidence — Profile Photo", level=3)
doc.image("rIdImgAvatar", align="center")

doc.heading("Supporting Evidence — LinkedIn Profile", level=3)
doc.image("rIdImgLinkedIn", align="center")

# Packaging into .docx ZIP
print("Writing document.xml...")
doc_xml = doc.build_xml()

content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="jpg" ContentType="image/jpeg"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>'''

rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

doc_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rIdImgLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/ar_logo.png"/>
  <Relationship Id="rIdImgBanner" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/anjali_banner.png"/>
  <Relationship Id="rIdImgPortfolio" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/portfolio_preview.png"/>
  <Relationship Id="rIdImgAvatar" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/anjali_avatar_circle.png"/>
  <Relationship Id="rIdImgLinkedIn" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/screenshot_linkedin.png"/>
</Relationships>'''

styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="22"/>
        <w:color w:val="1E293B"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:before="60" w:after="60" w:line="276" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>'''

settings_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="720"/>
</w:settings>'''

with zipfile.ZipFile(out_docx, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("[Content_Types].xml", content_types_xml)
    zf.writestr("_rels/.rels", rels_xml)
    zf.writestr("word/document.xml", doc_xml)
    zf.writestr("word/_rels/document.xml.rels", doc_rels_xml)
    zf.writestr("word/styles.xml", styles_xml)
    zf.writestr("word/settings.xml", settings_xml)
    
    # Add media files
    for r_id, (fname, mime) in img_files.items():
        fpath = os.path.join(base_dir, fname)
        zf.write(fpath, f"word/media/{fname}")

print(f"Successfully generated updated docx at: {out_docx}")
print(f"File size: {os.path.getsize(out_docx)} bytes")
