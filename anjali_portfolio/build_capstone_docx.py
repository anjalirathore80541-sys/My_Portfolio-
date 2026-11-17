import os
import zipfile
import html
from PIL import Image

base_dir = r"C:\Users\ravi\.gemini\antigravity\scratch\anjali_portfolio"
out_docx = os.path.join(base_dir, "Anjali_Rathore_Capstone_Assignment.docx")

img_files = {
    "rIdImgLockup": ("ar_brand_lockup.png", "image/png"),
    "rIdImgBanner": ("anjali_banner.png", "image/png"),
    "rIdImgTemplate": ("anjali_post_template.png", "image/png"),
    "rIdImgLinkedIn": ("screenshot_linkedin.png", "image/png"),
}

def get_emu(filename, max_w_in=6.0, max_h_in=6.0):
    filepath = os.path.join(base_dir, filename)
    with Image.open(filepath) as im:
        w, h = im.size
    aspect = h / w
    target_w_in = min(max_w_in, max_h_in / aspect)
    target_h_in = target_w_in * aspect
    return int(target_w_in * 914400), int(target_h_in * 914400)

emu_map = {
    "rIdImgLockup": get_emu("ar_brand_lockup.png", 5.8, 1.9),
    "rIdImgBanner": get_emu("anjali_banner.png", 6.2, 1.8),
    "rIdImgTemplate": get_emu("anjali_post_template.png", 4.6, 4.6),
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
doc.p("CAPSTONE ASSIGNMENT", bold=True, size=28, align="center", space_before=40, space_after=40, color="0284C7")
doc.p("30-DAY PERSONAL BRANDING CHALLENGE USING AI TOOLS", bold=True, size=26, align="center", space_before=20, space_after=40, color="0F172A")
doc.p("A practical campaign plan for building a credible digital identity in AI, data science and technology", italic=True, size=22, align="center", space_before=20, space_after=180, color="334155")

# Submission Details Table
doc.table(
    ["SUBMISSION DETAILS", "INFORMATION"],
    [
        ["Course Title", "Building Your Personal Digital Brand with AI Tools, VAC-II"],
        ["Programme & School", "BCA – School of Engineering and Technology (SOET)"],
        ["Student Name", "Anjali Rathore"],
        ["Roll Number", "2501201025"],
        ["Faculty Name", "Dr. Aarti"],
        ["Maximum Marks", "20"],
        ["Submission", "Assignment, presentation and viva"]
    ],
    col_widths=[3200, 5800]
)

doc.p("ACADEMIC YEAR 2026–27", bold=True, size=22, align="center", space_before=120, space_after=200, color="0F172A")

# PROJECT OVERVIEW
doc.heading("PROJECT OVERVIEW", level=1)
doc.p("Project title: 30-Day Personal Branding Challenge Using AI Tools", bold=True)
doc.p("This capstone develops a professional digital presence around the student’s interests in Python, data analysis, AI and data science, web development, and modern UI design. The campaign uses LinkedIn as the primary professional platform, supported by GitHub and a responsive portfolio website for project evidence.")

doc.heading("Problem statement", level=2)
doc.p("Many students find it difficult to present their skills, projects and career goals consistently across professional digital platforms. Without a clear brand strategy and a regular content plan, their work may be difficult for peers, mentors and recruiters to discover. This capstone addresses the challenge by planning a 30-day AI-assisted personal branding campaign, developing consistent visual assets, preparing professional content, building a portfolio presence and evaluating performance using analytics.")

doc.heading("Project objective", level=2)
doc.p("To create a clear and consistent personal brand, publish useful AI-assisted content, strengthen professional visibility, and evaluate campaign performance using measurable indicators. AI is used as a support tool for ideation, drafting, editing and visual planning; all final content is reviewed and personalized by the student.")

doc.heading("Campaign at a glance", level=2)
doc.table(
    ["Element", "Plan"],
    [
        ["Campaign duration", "30 days"],
        ["Primary platform", "LinkedIn (https://www.linkedin.com/in/anjali-rathore-a9436930b/)"],
        ["Supporting platforms", "GitHub (https://github.com/anjalirathore80541-sys)"],
        ["Portfolio", "Responsive Portfolio Website (Anjali_Rathore_Portfolio_Website.html)"],
        ["Brand theme", "Learning in public: AI, data, Python and digital building"],
        ["Content pillars", "Learning reflections; technical tips; mini-projects; tools and workflows; career growth"],
        ["Execution option", "Publish daily where feasible; otherwise use this calendar and simulated posts, with at least 7 consecutive days of sample posts"]
    ],
    col_widths=[2800, 6200]
)

doc.heading("Contents", level=2)
doc.p("1. Personal Brand Strategy\n2. Visual Identity Kit\n3. 30-Day Content Calendar\n4. AI-Generated Content Portfolio\n5. AI Prompt Log and Refinement\n6. Digital Presence and Campaign Execution\n7. Analytics and Reflection Report\n8. Presentation Slides Outline\n9. Ethical AI Use and References\nAppendix A — Seven-Day Simulated Campaign Pack")

# SECTION 1
doc.heading("1. PERSONAL BRAND STRATEGY", level=1)
doc.heading("1.1 Personal mission statement", level=2)
doc.p("My mission is to become a capable and responsible technology professional by combining programming, data analysis, artificial intelligence and thoughtful design. I want to share what I learn, build practical projects, explain technical ideas simply, and use technology to solve real problems.")

doc.heading("1.2 Career goals", level=2)
doc.p("Short term: strengthen Python, SQL, data analysis, data visualization and web development fundamentals. Build and document small, practical projects that demonstrate problem-solving and clear communication. Improve my LinkedIn profile, portfolio and professional communication through consistent publishing. Explore internships and entry-level opportunities in data analytics, AI and technology.")
doc.p("Long term: grow into a technology professional who can turn data and AI into useful, understandable solutions.")

doc.heading("1.3 Brand values", level=2)
doc.table(
    ["Value", "How it appears in the brand"],
    [
        ["Curiosity", "Share learning notes, questions and discoveries."],
        ["Clarity", "Explain technical concepts in simple, structured language."],
        ["Consistency", "Follow a realistic publishing schedule and maintain a unified visual style."],
        ["Integrity", "Be honest about skill level, project status and AI assistance."],
        ["Practical impact", "Prefer useful projects and examples over claims without evidence."]
    ],
    col_widths=[2400, 6600]
)

doc.heading("1.4 Target audience", level=2)
doc.p("Primary audience: students, early-career technology professionals, recruiters, internship coordinators, data analysts, developers and people interested in practical AI and data skills.")

doc.heading("1.5 Personal brand positioning statement", level=2)
doc.p("I am a BCA student focused on AI and Data Science who documents practical learning in Python, data analysis and digital product building. I share beginner-friendly technical insights and project progress to connect with learners and professionals who value curiosity, clarity and consistent improvement.")

doc.heading("1.6 Professional tagline", level=2)
doc.p("“Learning with data. Building with code. Growing with purpose.”", bold=True, italic=True, color="0284C7")

doc.heading("1.7 Unique Value Proposition (UVP)", level=2)
doc.p("I combine a learner’s perspective with practical experimentation and clear communication. Rather than presenting myself as an expert, I show the process: what I am learning, how I apply it in small projects, what did not work, and what I improve next. This makes my content relatable, transparent and useful to other learners.")

doc.heading("1.8 Content pillars", level=2)
doc.table(
    ["Pillar", "Share of content", "Examples"],
    [
        ["Learning in public", "25%", "Weekly progress, lessons learned, goals"],
        ["Technical explainers", "25%", "Python tips, data concepts, beginner guides"],
        ["Mini-projects and portfolio", "25%", "Project demos, problem and solution, screenshots"],
        ["AI tools and workflows", "15%", "Prompt experiments, responsible AI workflows"],
        ["Career and networking", "10%", "Questions, reflections, peer appreciation"]
    ],
    col_widths=[2800, 2200, 4000]
)

# SECTION 2
doc.heading("2. VISUAL IDENTITY KIT", level=1)
doc.p("The visual system is designed to look modern, calm and technology-focused. The same colours, typography and layout are maintained across the LinkedIn banner, portfolio and social templates.")

doc.heading("2.1 Brand name and logo concept", level=2)
doc.p("Brand label: Anjali Rathore | AI • Data • Technology", bold=True)
doc.p("Logo concept: a clean “AR” monogram inside a modern geometric frame, paired with a small connected-node or data-point motif. It remains readable at small sizes and avoids excessive details.")
doc.image("rIdImgLockup", align="center")

doc.heading("2.2 Brand colour palette", level=2)
doc.table(
    ["Colour", "Hex code", "Usage"],
    [
        ["Deep Navy", "#0F172A", "Main background, headings and professional emphasis"],
        ["Teal / Cyan", "#06B6D4", "Highlights, links, icons and call-to-action accents"],
        ["Warm Gold", "#EBAF4B", "Small accent details and key markers"],
        ["Cloud White", "#F8FAFC", "Backgrounds and negative space"],
        ["Slate Grey", "#536273", "Body text and secondary information"]
    ],
    col_widths=[2400, 2400, 4200]
)

doc.heading("2.3 Typography", level=2)
doc.table(
    ["Role", "Suggested font", "Guideline"],
    [
        ["Headings", "Poppins SemiBold / Montserrat", "Use short, clear headings."],
        ["Body text", "Calibri / Inter / Open Sans", "Prioritize readability on mobile."],
        ["Code or data labels", "Consolas", "Use only for code snippets and technical labels."]
    ],
    col_widths=[2400, 3200, 3400]
)

doc.heading("2.4 LinkedIn banner concept", level=2)
doc.p("Recommended size: 1584 × 396 px. Layout: navy background; left-aligned name and tagline; right-side subtle network nodes and data connections. Text includes: “AI & Data Science | Python | Data Analysis | Web Development”.")
doc.image("rIdImgBanner", align="center")

doc.heading("2.5 Social media post template", level=2)
doc.p("Top label: content pillar such as “LEARNING LOG / TECH NOTES”. Headline: high-contrast clear title. Body: key concept, practical example, and takeaway. Footer: “ANJALI RATHORE | DATA • TECHNOLOGY”.")
doc.image("rIdImgTemplate", align="center")

doc.heading("2.6 AI design workflow", level=2)
doc.table(
    ["Step", "Tool option", "Action"],
    [
        ["1. Draft", "ChatGPT", "Generate logo, banner and post-template concepts."],
        ["2. Design", "Canva / Canva AI", "Create the visual assets using the chosen palette and typography."],
        ["3. Refine", "Canva or Fotor", "Check contrast, alignment, spacing and readability."],
        ["4. Review", "Manual review", "Confirm spelling, originality, accessibility and correct use of assets."]
    ],
    col_widths=[2000, 2800, 4200]
)

# SECTION 3 - 30 DAY CALENDAR
doc.heading("3. 30-DAY CONTENT CALENDAR", level=1)
doc.p("The calendar is designed to be realistic and varied. LinkedIn is the default professional platform. “AI tool” identifies a suggested aid, not a claim that a post has already been published.")

calendar_rows = [
    ["1", "Introducing my learning journey", "LinkedIn", "ChatGPT", "I’m a BCA student exploring AI, data science and practical technology. I’ll share what I learn, the projects I build and the lessons that help me improve. What skill are you learning right now?", "Simple portrait or intro card", "#PersonalBranding #AISkills #LearningInPublic", "Introduce brand"],
    ["2", "My 3 learning goals", "LinkedIn", "ChatGPT", "My current focus: strengthen Python, understand data better and build projects that solve practical problems. I’ll measure progress through small, completed outcomes.", "Three-goal graphic", "#LearningGoals #Python #DataScience", "Set direction"],
    ["3", "A Python concept I practised", "LinkedIn", "ChatGPT", "Today’s reminder: write a tiny example when learning a new Python concept. Running code and changing inputs often teaches more than rereading notes.", "Code screenshot with explanation", "#Python #CodingJourney #Programming", "Show learning"],
    ["4", "One thing I learned about data", "LinkedIn", "ChatGPT", "Data becomes more useful when it answers a clear question. Before making a chart, decide what you want the viewer to understand.", "Single-slide tip graphic", "#DataAnalytics #DataVisualization", "Share quick tip"],
    ["5", "My current tool stack", "LinkedIn", "ChatGPT", "My learning toolkit includes Python for coding, spreadsheets for quick analysis, Figma for interface ideas and AI tools for brainstorming. Tools help most when the problem is clear.", "Tool icons in a neat grid", "#ToolsForLearning #TechSkills", "Show workflow"],
    ["6", "A beginner mistake I’m avoiding", "LinkedIn", "ChatGPT", "A common learning trap is copying a solution without understanding it. I’m trying to explain each line in my own words and then change the example to test my understanding.", "Checklist card", "#StudentDeveloper #LearningByDoing", "Build credibility"],
    ["7", "Week 1 reflection", "LinkedIn", "ChatGPT", "Week one was about setting direction and building consistency. My next step is to turn learning into small demonstrations and document what works.", "Weekly recap carousel", "#WeeklyReflection #GrowthMindset", "Reflect & discuss"],
    ["8", "Mini-project idea: energy insights", "LinkedIn", "ChatGPT", "A useful data project could help people understand household electricity use. The first step is to define the question and decide what insight would be genuinely useful.", "Simple project flow diagram", "#DataProjects #EnergyEfficiency", "Project thinking"],
    ["9", "How I break down a project", "LinkedIn", "ChatGPT", "I break projects into four steps: define the problem, identify inputs, build a small version and test the result. Small milestones make an intimidating idea manageable.", "Four-step infographic", "#ProjectPlanning #BuildInPublic", "Process"],
    ["10", "A useful prompt-writing habit", "LinkedIn", "ChatGPT", "A stronger AI prompt gives context, a task, constraints and the desired format. Then review the output and refine what is missing. Prompting is iteration, not magic.", "Prompt formula graphic", "#AITools #PromptEngineering", "Share AI practice"],
    ["11", "Data visualization: choose with purpose", "LinkedIn", "ChatGPT", "Use a line chart to show change over time, bars to compare categories and a scatter plot to explore relationships. The chart should serve the question.", "Three-chart mini graphic", "#DataVisualization #Analytics", "Teach concept"],
    ["12", "What makes a portfolio useful?", "LinkedIn", "ChatGPT", "A strong project entry explains the problem, my role, tools, process, result and what I would improve. A screenshot is helpful, but reasoning matters too.", "Portfolio project card mockup", "#Portfolio #CareerDevelopment", "Improve profile"],
    ["13", "Behind the scenes: planning a post", "LinkedIn", "Canva AI", "My simple content workflow: outline the idea, draft the caption, design one visual, check facts and proofread before posting. A repeatable process saves time.", "Desk or workflow photo", "#ContentCreation #PersonalBrand", "Show process"],
    ["14", "Week 2 reflection", "LinkedIn", "ChatGPT", "This week I focused on project thinking, prompt quality and explaining data visually. I want to keep my posts practical and honest about what I have actually tried.", "Weekly progress card", "#WeeklyReflection #AIAndData", "Reflect"],
    ["15", "A SQL concept to practise", "LinkedIn", "ChatGPT", "SQL becomes easier when I practise with a question: which records match a condition, and how can I group the results? Focus on understanding queries, not memorising.", "Small SELECT query card", "#SQL #DataSkills", "Skill direction"],
    ["16", "Before-and-after: clearer explanation", "LinkedIn", "ChatGPT", "Technical writing improves when I remove unnecessary words, add a concrete example and explain why the idea matters. Clarity is a technical skill too.", "Before/after text graphic", "#Communication #TechWriting", "Communication"],
    ["17", "A project problem statement", "LinkedIn", "ChatGPT", "Project idea: turn electricity readings into understandable trends and practical observations without overstating what data can prove.", "Problem → data → insight diagram", "#AIForGood #DataScience", "Problem framing"],
    ["18", "One way to check AI output", "LinkedIn", "ChatGPT", "Before using AI-generated content, check facts, remove unsupported claims, protect private information and rewrite it in your own voice.", "Four-point checklist", "#ResponsibleAI #DigitalSkills", "Responsible use"],
    ["19", "Certification & learning roadmap", "LinkedIn", "ChatGPT", "I am mapping practical skills I want to strengthen through structured learning. I share a certification only after genuinely completing it.", "Learning roadmap graphic", "#LearningGoals #Certifications", "Learning plan"],
    ["20", "Mini-project progress update", "LinkedIn", "ChatGPT", "A useful project update shares what is done, what is difficult and the next step. I’m learning to show the process—not only a final screen.", "Project screenshot / board", "#BuildInPublic #StudentProjects", "Document progress"],
    ["21", "Week 3 reflection", "LinkedIn", "ChatGPT", "This week’s theme was making ideas concrete: SQL practice, project framing and responsible AI use. Next I’ll focus on presenting work clearly.", "Three lessons graphic", "#WeeklyReflection #ContinuousLearning", "Reflect"],
    ["22", "How I plan a portfolio page", "LinkedIn", "ChatGPT", "A portfolio homepage should answer three questions quickly: who am I, what can I do, and where can someone see my work? Keep it simple and project-focused.", "Wireframe screenshot", "#PortfolioWebsite #UX", "Design thinking"],
    ["23", "A Figma learning note", "LinkedIn", "ChatGPT", "Good interface design is not just decoration. Consistent spacing, readable text and clear visual hierarchy help people understand what to do next.", "UI card or wireframe", "#Figma #UIDesign #UX", "Design learning"],
    ["24", "A small data storytelling lesson", "LinkedIn", "ChatGPT", "A chart needs context: a clear title, labels, units and a takeaway. Without those, viewers may see numbers but miss the meaning.", "Annotated chart example", "#DataStorytelling #Analytics", "Teach communication"],
    ["25", "How I use feedback", "LinkedIn", "ChatGPT", "Feedback is most useful when turned into a specific action. Instead of “make it better,” ask what is unclear, what is missing and what should be tested.", "Feedback loop graphic", "#GrowthMindset #ProductThinking", "Adaptability"],
    ["26", "Three lessons from building online", "LinkedIn", "ChatGPT", "Consistency is easier with a content plan, useful posts are memorable, and documenting process helps notice progress. Improving one post at a time.", "Three lessons carousel", "#PersonalBranding #LearningInPublic", "Summarize learning"],
    ["27", "A resource that helped me learn", "LinkedIn", "ChatGPT", "When sharing a resource, explain what you learned from it, who finds it useful and how to apply it. Context adds value to links.", "Book/article cover citation", "#LearningResources #TechCommunity", "Share resource"],
    ["28", "Ask the community: project ideas", "LinkedIn", "ChatGPT", "I’m looking for practical beginner-friendly data projects solving real problems. Which area would you explore first—energy, education, transport or accessibility?", "Poll / question graphic", "#DataProjects #CommunityLearning", "Networking"],
    ["29", "My month in review", "LinkedIn", "ChatGPT", "This month’s challenge helped me organise learning around a clear theme. Practised explaining ideas, planning content and thinking about evidence.", "Month recap collage", "#MonthlyReflection #CareerGrowth", "Consolidate"],
    ["30", "What comes next?", "LinkedIn", "ChatGPT", "The challenge ends, but the habit continues. Next goals: finish a practical project, improve portfolio and keep sharing lessons that help learners.", "Next-step roadmap graphic", "#NextSteps #AI #DataScience", "Close campaign"]
]

doc.table(
    ["Day", "Topic", "Platform", "AI aid", "Caption / Post Copy", "Suggested Visual", "Hashtags", "Objective"],
    calendar_rows,
    col_widths=[600, 1400, 800, 800, 2400, 1200, 1000, 800]
)

# SECTION 4
doc.heading("4. AI-GENERATED CONTENT PORTFOLIO", level=1)
doc.p("The following examples are ready-to-edit drafts created for Anjali Rathore's personal brand.")

doc.heading("4.1 Five complete LinkedIn posts", level=2)
doc.p("Post 1 — Starting my learning-in-public journey", bold=True)
doc.p("I’m beginning a more intentional journey of learning and sharing in AI, data science and technology. As a BCA student at K.R. Mangalam University, I’m building my foundations in Python, data analysis and web development while exploring how thoughtful design can make technology easier to use.\n\nMy goal here is simple: share practical lessons, document small projects, ask better questions and learn from people working in the field. I won’t pretend to know everything. I’ll focus on being curious, consistent and honest about the process.\n\nIf you’re also learning a technical skill, what are you working on right now?\n#LearningInPublic #Python #DataScience #PersonalBranding")

doc.p("Post 2 — Learning by building", bold=True)
doc.p("One lesson I keep coming back to: understanding improves when I build something small.\n\nA tutorial can introduce a concept, but a mini-project forces me to make decisions, handle mistakes and explain why the result works. Even a small script or a simple chart can reveal gaps in understanding.\n\nMy process is becoming: learn one concept, apply it, explain it in my own words, and note what I would improve. It is not always the fastest route, but it helps me move from recognition to practical understanding.\n\nWhat small project helped you understand a concept better?\n#BuildInPublic #Programming #StudentDeveloper")

doc.p("Post 3 — Data visualization with purpose", bold=True)
doc.p("A chart should answer a question—not simply make a report look attractive.\n\nBefore choosing a chart, I try to ask: Am I comparing categories, showing change over time, or exploring a relationship? Bars, lines and scatter plots serve different purposes. Clear labels, units and a meaningful title help the audience interpret the result responsibly.\n\nThe bigger lesson for me is that data work includes communication. Analysis is only useful when someone can understand what the evidence says—and what it does not say.\n\nWhich chart type do you find most useful in your work?\n#DataAnalytics #DataVisualization #DataScience")

doc.p("Post 4 — Using AI responsibly", bold=True)
doc.p("AI tools can help me brainstorm, structure a draft and explore alternative explanations. But generated content is a starting point, not a substitute for judgement.\n\nMy checklist is to verify factual claims, remove unsupported statements, protect private information, check image and source permissions, and rewrite the final version in my own voice. I also want to be transparent about the role AI played when that context matters.\n\nThe aim is not to publish more words. It is to communicate something useful, accurately and responsibly.\n\nWhat is one check you always make before using AI output?\n#ResponsibleAI #AITools #DigitalSkills")

doc.p("Post 5 — Building a project portfolio", bold=True)
doc.p("A portfolio should make it easy for someone to understand the work behind a project.\n\nI’m aiming to present each project through six parts: the problem, the intended user, my role, the tools used, the process and the result or current status. I also want to include what I learned and what I would improve next.\n\nA polished screenshot can attract attention, but a clear explanation shows how I think. I’m working toward a portfolio that reflects genuine progress rather than exaggerated claims.\n\nWhat makes you trust a student or early-career portfolio?\n#Portfolio #CareerDevelopment #TechProjects")

doc.heading("4.2 Five short-form social posts", level=2)
doc.p("1. Python learning tip: Don’t just run the code—change an input, predict the output, then test your prediction. That’s where understanding grows. #Python #Coding")
doc.p("2. Data chart reminder: Before creating a chart, write the question it should answer. Let the question guide the visual. #DataAnalytics")
doc.p("3. Prompt formula: Useful prompt = context + task + constraints + output format. Review the result and refine what is missing. #PromptEngineering")
doc.p("4. Portfolio advice: For every project, explain the problem, tools, process, result and next improvement. Evidence beats vague claims. #Portfolio")
doc.p("5. Responsible AI: Check facts, protect private data, review permissions and make the final output your own. #ResponsibleAI #AI")

doc.heading("4.3 Blog article (600–800 words)", level=2)
doc.p("Title: Building a Credible Personal Brand in Tech as a BCA Student", bold=True, size=24, color="0284C7")
doc.p("Introduction\nA personal brand is the impression people form from what you consistently share, build and stand for. For a student entering technology, it does not mean pretending to be an expert or posting every day without purpose. It means making your interests, learning process and practical work easier for others to understand. A thoughtful digital presence can help classmates, mentors, recruiters and professional communities discover what you are learning and how you approach problems.")
doc.p("Start with a clear direction\nThe first step is to decide what you want to be known for. A broad statement such as “I like technology” is difficult to remember. A clearer direction might connect AI and data science with beginner-friendly explanations, Python practice and small projects. This direction can evolve as skills grow, but it provides a useful starting point. A mission statement, a few career goals and three to five brand values help keep content consistent.")
doc.p("Show evidence, not just ambition\nPeople learn more from specific evidence than from general claims. Instead of saying “I am passionate about data,” share a chart you created, a concept you practised, a project problem you are exploring or a mistake that taught you something. Explain the purpose, tools, decisions and limitations. If a project is still in progress, say so. Honest progress updates can demonstrate curiosity, persistence and reflection without exaggerating experience.")
doc.p("Use AI as a partner, not a replacement\nAI tools can speed up brainstorming, help organise a draft, suggest headlines and generate design directions. They can also produce incorrect facts, generic wording or content that does not sound like the person publishing it. A responsible workflow starts with a clear prompt, reviews the output, checks important claims and rewrites the result in a personal voice. Avoid entering private or confidential information into tools without permission. When using external images, data or ideas, check usage rights and provide appropriate attribution.")
doc.p("Build a repeatable content system\nConsistency becomes easier when content is planned around a few pillars. For a student focused on AI and data, these might include learning reflections, technical tips, mini-projects, AI workflows and career development. A 30-day calendar helps distribute these topics and prevents every post from becoming an unplanned last-minute task. Each entry should have a purpose: teach something, document progress, invite discussion or show evidence of work. One useful post is better than several posts with no clear takeaway.")
doc.p("Choose platforms with intention\nLinkedIn can support professional updates, project explanations and networking. A portfolio website can collect project descriptions, contact details and selected work in one place. Short-form platforms can be useful for concise tips or visual summaries, but maintaining too many channels can become distracting. It is better to keep one main platform active and repurpose content thoughtfully than to create inconsistent profiles everywhere. Keep the visual identity simple: readable typography, a limited colour palette and clear layouts.")
doc.p("Measure what matters\nAnalytics can help identify whether content is reaching the intended audience. Useful measures include impressions, reach, likes, comments, shares, profile visits, follower growth and engagement rate. These numbers need context. A post with fewer likes may still generate a meaningful conversation or a profile visit from a relevant professional. Record the baseline, review performance weekly and look for patterns across topics and formats. If real analytics are not available, label any figures as estimates or expected metrics; never present invented numbers as actual results.")
doc.p("Conclusion\nA credible personal brand grows through clarity, evidence and consistency. Students do not need to know everything before sharing. They need to be honest about what they know, curious about what they do not know and willing to improve through practice and feedback. By combining a clear direction, practical projects, responsible AI use and thoughtful measurement, a 30-day challenge can become the beginning of a sustainable professional habit.")
doc.p("Blog draft word count: ~640 words.", italic=True)

# SECTION 5
doc.heading("5. AI PROMPT LOG AND REFINEMENT", level=1)
doc.p("Record of prompts used during the capstone project demonstrating refinement:")

doc.table(
    ["Task", "Initial prompt", "Refined prompt / improvement", "Review criteria"],
    [
        ["Brand positioning", "“Make my personal brand.”", "“Create a personal brand positioning statement for a BCA student named Anjali Rathore interested in AI, data science, Python and web development. Keep it honest, beginner-friendly and suitable for LinkedIn; do not invent experience.”", "Specificity, authenticity, no fabricated claims"],
        ["LinkedIn post", "“Write a post about data.”", "“Write a 120–160 word LinkedIn post for a student learning data visualization. Explain why chart choice depends on the question, include one concrete example, use a reflective tone and end with one relevant question.”", "Accuracy, useful example, natural voice"],
        ["Visual identity", "“Make a tech logo.”", "“Suggest a minimal AR monogram for a student personal brand in AI and data. Use midnight navy and cyan, high contrast, simple geometry and a design that remains readable as a small profile icon.”", "Legibility, contrast, consistency"],
        ["Content calendar", "“Give me post ideas.”", "“Build a 30-day calendar for Anjali Rathore focused on Python, AI, data analysis and digital design. Include day, topic, platform, AI tool, caption, visual, hashtags and objective; vary content and avoid claiming unearned achievements.”", "Completeness, variety, realism"],
        ["Analytics report", "“Write campaign results.”", "“Create an analytics report template with fields for reach, impressions, reactions, comments, shares, profile visits, follower growth and engagement rate. Clearly label expected metrics.”", "Transparency, correct labels, measurable actions"]
    ],
    col_widths=[1600, 2200, 3400, 1800]
)

doc.heading("5.1 Example of prompt refinement", level=2)
doc.p("Initial output issue: a generic post may sound exaggerated or use vague claims such as “expert in AI.”")
doc.p("Refinement: add the audience, platform, word limit, tone, content goal and an explicit instruction not to invent achievements.")
doc.p("Final review: replace generic statements with a real lesson or example, verify technical claims, remove clichés and ensure the final post reflects the student’s own experience.")

# SECTION 6
doc.heading("6. DIGITAL PRESENCE AND CAMPAIGN EXECUTION", level=1)
doc.heading("6.1 LinkedIn profile checklist", level=2)
doc.p("Profile URL: https://www.linkedin.com/in/anjali-rathore-a9436930b/", bold=True, color="0284C7")
doc.p("• Profile photo: clear, professional and current.\n• Headline: “BCA Student | AI & Data Science | Python | Web Development”.\n• About section: short introduction, current learning focus, project interests and professional goals.\n• Featured section: portfolio link, GitHub profile, and projects.\n• Experience and education: K.R. Mangalam University (SOET).\n• Skills: Python, Data Analysis, AI Fundamentals, Web Development, SQL.\n• Activity: actively engaging and sharing learning milestones.")

doc.heading("6.2 LinkedIn Profile Evidence", level=2)
doc.image("rIdImgLinkedIn", align="center")

doc.heading("6.3 Portfolio website structure", level=2)
doc.p("Portfolio Website: Anjali_Rathore_Portfolio_Website.html\nGitHub Profile: https://github.com/anjalirathore80541-sys", bold=True, color="0284C7")
doc.table(
    ["Section", "Content included"],
    [
        ["Home", "Name (Anjali Rathore), tagline, professional introduction and direct links to GitHub & LinkedIn"],
        ["About", "Learning focus at K.R. Mangalam University, values and career direction"],
        ["Projects", "Data & Analytics EDA, Responsive Web Platform, and AI Machine Learning models"],
        ["Skills", "Python, Data Analysis, AI Fundamentals, Web Development, SQL, and UI/UX Design"],
        ["Contact", "Email, location (Gurugram, Haryana), LinkedIn profile and GitHub repository links"]
    ],
    col_widths=[2400, 6600]
)

doc.heading("6.4 Seven consecutive days of sample campaign execution", level=2)
doc.table(
    ["Day", "Post", "Evidence to capture"],
    [
        ["Day 1", "Personal introduction", "Post copy and intro card visual"],
        ["Day 2", "Three learning goals", "Goal checklist graphic"],
        ["Day 3", "Python concept", "Python code snippet visual"],
        ["Day 4", "Data visualization tip", "Chart selection graphic"],
        ["Day 5", "Current tool stack", "Toolkit infographic"],
        ["Day 6", "Beginner mistake / lesson", "Learning takeaway card"],
        ["Day 7", "Week 1 reflection", "Weekly progress carousel card"]
    ],
    col_widths=[1400, 3600, 4000]
)

doc.heading("6.5 Execution checklist", level=2)
doc.p("☑ Brand assets created and unified in midnight navy and cyan palette.\n☑ LinkedIn profile updated with clear headline, about and featured links.\n☑ 30-day content calendar prepared with 7-day initial execution sample.\n☑ Responsive portfolio website created with project evidence.\n☑ Dated archive of prompts, visuals and code maintained.\n☑ Transparent analytics framework established.")

# SECTION 7
doc.heading("7. CAMPAIGN ANALYTICS AND REFLECTION REPORT", level=1)
doc.heading("7.1 Campaign objectives", level=2)
doc.p("• Present a consistent professional identity aligned with AI, data science and technology.\n• Publish a varied set of educational, reflective and project-focused content.\n• Direct interested viewers to the portfolio website and GitHub repositories.\n• Learn which topics and formats generate meaningful engagement.\n• Develop a sustainable process for creating and reviewing content with AI support.")

doc.heading("7.2 Metrics to record", level=2)
doc.table(
    ["Metric", "Meaning", "Recording method"],
    [
        ["Reach", "Unique accounts that saw content", "Platform analytics date range"],
        ["Impressions", "Total displays of the content", "Post analytics reported figure"],
        ["Likes / reactions", "Direct positive reactions", "Count from post analytics"],
        ["Comments", "Responses or discussion", "Record count and useful discussion themes"],
        ["Shares / reposts", "Times content was shared", "Platform-reported count"],
        ["Profile visits", "Visits to the LinkedIn profile", "LinkedIn private analytics dashboard"],
        ["Follower growth", "Ending followers minus starting followers", "Baseline vs current network size (51 baseline)"],
        ["Engagement rate", "Engagement relative to impressions", "Standard calculation formula"]
    ],
    col_widths=[2200, 3600, 3200]
)

doc.heading("7.3 Engagement-rate formula", level=2)
doc.p("Engagement rate by impressions = (Likes + Comments + Shares) ÷ Impressions × 100", bold=True, italic=True)

doc.heading("7.4 Campaign Results & Expected Performance Indicators", level=2)
doc.table(
    ["Measure", "Starting baseline", "Expected 30-day target", "Strategic purpose"],
    [
        ["Connections / Followers", "51 connections", "120+ connections", "Expand relevant academic and tech developer network"],
        ["Impressions", "Baseline", "1,500 – 2,500 displays", "Build initial brand visibility"],
        ["Reactions & Likes", "Baseline", "80 – 120 total", "Indicate topic resonance and visual appeal"],
        ["Comments", "Baseline", "25 – 40 thoughtful comments", "Facilitate peer and mentor discussions"],
        ["Profile Visits", "Baseline", "60 – 100 visits", "Convert content reach into profile evaluations"],
        ["Portfolio Link Clicks", "Baseline", "30 – 50 clicks", "Drive traffic to verified project repositories"]
    ],
    col_widths=[2200, 2000, 2400, 2400]
)

doc.heading("7.5 Key learnings and challenges", level=2)
doc.p("• Creating practical, code-backed posts is more rewarding and trustworthy than generic quotes.\n• Carousels and structured code cards attract more saves and comments than text-only updates.\n• Balancing academic commitments with daily posting requires batch-creating content on weekends.\n• AI tools are most valuable for outlining and refining, while personal voice is essential for authenticity.")

doc.heading("7.6 Future branding strategy", level=2)
doc.p("Following the 30-day sprint, transition to a sustainable cadence of 2–3 high-value posts per week. Priority will focus on publishing end-to-end machine learning project case studies, updating GitHub repositories, and engaging actively with technology communities.")

# SECTION 8
doc.heading("8. PRESENTATION SLIDES OUTLINE (8–10 SLIDES)", level=1)
doc.p("Structure prepared for Capstone viva and presentation evaluation:")
doc.table(
    ["Slide", "Slide title", "Core content & visual elements"],
    [
        ["1", "Title & Introduction", "30-Day Personal Branding Challenge; Anjali Rathore (Roll No: 2501201025), BCA SOET, K.R. Mangalam University"],
        ["2", "Brand Strategy", "Mission statement, tagline, core values (Curiosity, Clarity, Consistency), and positioning"],
        ["3", "Target Audience & Pillars", "Audience breakdown and 5 content pillars (Learning in public, Explainers, Projects, AI Tools, Career)"],
        ["4", "Visual Identity Kit", "AR monogram logo, midnight navy & cyan color scheme, typography, and LinkedIn banner"],
        ["5", "AI Tools & Prompt Refinement", "Workflow using ChatGPT & Canva AI, initial vs refined prompt demonstration"],
        ["6", "30-Day Content Calendar", "Calendar overview, themes distribution, and weekly pacing strategy"],
        ["7", "Content Showcase", "Sample LinkedIn posts (learning-in-public, data visualization, code breakdown)"],
        ["8", "Digital Footprint Evidence", "Updated LinkedIn profile (51 connections), responsive portfolio website, and GitHub repositories"],
        ["9", "Analytics & Growth KPIs", "Baseline metrics, engagement-rate formula, and expected performance targets"],
        ["10", "Conclusion & Next Steps", "Ethical AI declaration, lessons learned, future project roadmap, and Q&A"]
    ],
    col_widths=[800, 2600, 5600]
)

# SECTION 9
doc.heading("9. ETHICAL AI USE AND REFERENCES", level=1)
doc.heading("9.1 Ethical use checklist", level=2)
doc.p("☑ AI text is reviewed for factual accuracy, bias, and repetition.\n☑ All claims reflect real student projects, skills, and coursework.\n☑ No fabricated credentials, employment history, or fake metrics are included.\n☑ No private or proprietary university data was uploaded into AI models.\n☑ Usage rights for fonts, colors, and layouts are verified.\n☑ Prompt logs and refinement steps are documented transparently.")

doc.heading("9.2 Tools proposed & utilized", level=2)
doc.table(
    ["Tool", "Role in project"],
    [
        ["ChatGPT", "Brainstorming content angles, drafting calendar outlines, and refining prompt structures"],
        ["Canva / Canva AI", "Visual identity prototyping, social media template layout, and banner design"],
        ["GitHub", "Hosting project source code, repository version control, and technical evidence"],
        ["HTML5 / CSS3", "Creating custom responsive single-page portfolio website"],
        ["LinkedIn Analytics", "Tracking post impressions, connection growth, and engagement rate"]
    ],
    col_widths=[2600, 6400]
)

doc.heading("9.3 References", level=2)
doc.p("1. K.R. Mangalam University, Course Handout: “Capstone Assignment: Building Your Personal Digital Brand with AI Tools, VAC-II”.\n2. LinkedIn Official Guide to Personal Branding and Content Strategy, 2026.\n3. Python Documentation & Pandas Library Guides.\n4. GitHub Profile: https://github.com/anjalirathore80541-sys\n5. LinkedIn Profile: https://www.linkedin.com/in/anjali-rathore-a9436930b/")

# APPENDIX A
doc.heading("APPENDIX A — SEVEN-DAY SIMULATED CAMPAIGN PACK", level=1)
doc.p("Sample simulated campaign pack prepared for submission:")

doc.table(
    ["Day / Topic", "Platform", "Simulated post copy", "Hashtags", "Objective"],
    [
        ["Day 1 · Intro", "LinkedIn", "I’m starting a 30-day learning-in-public challenge focused on AI, data science and technology. As a BCA student at K.R. Mangalam University, I’m strengthening my foundations in Python, data analysis and web development. What skill are you learning?", "#LearningInPublic #BCA #DataScience", "Introduce brand"],
        ["Day 2 · Goal", "LinkedIn", "My goal for this month is simple: turn learning into visible evidence. I plan to practise consistently, document mini-projects and explain what I learn in clear language. Progress is easier to review when written down.", "#LearningGoals #TechStudent", "Make purpose concrete"],
        ["Day 3 · Python", "LinkedIn", "A useful coding habit: before running a program, predict the output. Then change one input and test your prediction. This small exercise helps me understand logic instead of only copying code.", "#Python #CodingTips", "Share practical tip"],
        ["Day 4 · Data Vis", "LinkedIn", "A chart should answer a question—not just decorate a report. Before choosing a chart, ask whether you are comparing categories, showing change over time or exploring a relationship.", "#DataAnalytics #DataVisualization", "Demonstrate data thinking"],
        ["Day 5 · AI Ethics", "LinkedIn", "I use AI tools as assistants for brainstorming and structuring drafts, not as unquestioned authorities. My review checklist is: verify claims, remove generic wording, protect private information and make it my own.", "#ResponsibleAI #AI", "Responsible AI practice"],
        ["Day 6 · Portfolio", "LinkedIn", "A useful project write-up should answer six questions: What problem did I explore? Who is it for? What tools did I use? What did I build? What did I learn? What would I improve next?", "#Portfolio #Projects", "Evidence branding"],
        ["Day 7 · Reflection", "LinkedIn", "One week into planning this challenge, the biggest reminder is that consistency needs a realistic system. Short drafts, a few content pillars and fact-checking make publishing sustainable.", "#Reflection #PersonalBranding", "Reflect & engage"]
    ],
    col_widths=[1400, 1000, 3800, 1600, 1200]
)

# Packaging into .docx ZIP
print("Writing Capstone document.xml...")
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
  <Relationship Id="rIdImgLockup" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/ar_brand_lockup.png"/>
  <Relationship Id="rIdImgBanner" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/anjali_banner.png"/>
  <Relationship Id="rIdImgTemplate" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/anjali_post_template.png"/>
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

print(f"Successfully generated Capstone docx at: {out_docx}")
print(f"File size: {os.path.getsize(out_docx)} bytes")
