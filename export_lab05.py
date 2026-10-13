"""Export the supplied answers and tested implementation as a submission PDF."""
from pathlib import Path
import subprocess
from xml.sax.saxutils import escape

import fitz
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted

ROOT = Path(__file__).resolve().parent
source = fitz.open(ROOT / 'IT24100315_LAB05_IS.pdf')
text = '\n'.join(page.get_text() for page in source)
styles = getSampleStyleSheet()
styles['BodyText'].fontSize = 10
styles['BodyText'].leading = 14
styles['Code'].fontSize = 8
styles['Code'].leading = 11
story = [Paragraph('Lab 05: Local Search Algorithms', styles['Title']),
         Paragraph('HRM A A BANDARA | IT24100315 | SE3062 Intelligent Systems', styles['BodyText']),
         Spacer(1, 16)]

def paragraph(value):
    story.append(Paragraph(escape(value).replace('\n', '<br/>'), styles['BodyText']))
    story.append(Spacer(1, 8))

# Retain the student's recorded observations and MCQ responses verbatim.
answers = text.split('Section 1: ')[1].split('Section 3: ')[0]
for block in answers.split('\n\n'):
    paragraph(block.strip())

story.append(Paragraph('Part C: Completed implementation', styles['Heading1']))
paragraph('The supplied PDF test runner contains only random.seed(42). The implementation below completes its generate-evaluate-prune cycle. A separate reproducible parabola check was added; it checks a tolerance of 2 around x = 50, since random successors do not guarantee the exact maximum.')
story.append(Preformatted((ROOT / 'local_beam_search.py').read_text(), styles['Code']))
story.append(Paragraph('Exact test output', styles['Heading2']))
output = subprocess.check_output(['python', str(ROOT / 'local_beam_search.py')], text=True)
story.append(Preformatted(output, styles['Code']))
story.append(Paragraph('Discussion: Beam search versus independent hill climbing', styles['Heading2']))
paragraph('Local Beam Search pools successors from all three states and selects the best three overall. All selected states can descend from one parent and converge on the same region. Three independent Hill Climbing runs select a neighbour separately for each run, so one run cannot replace the others. Independent runs generally retain more diversity, although they may still reach the same peak.')
story.append(Paragraph('Discussion: Expensive objective with a fixed evaluation budget', styles['Heading2']))
paragraph('I would choose Simulated Annealing, which evaluates one proposed neighbour per iteration. I would enforce an evaluation counter and stop when the budget is exhausted, using a moderate initial temperature and a cooling rate matched to that budget. For B moves and desired final temperature Tf, choose alpha = (Tf / T0) ** (1 / B). The recorded 0.50 run stopped after 8 steps, whereas 0.99 explored for 528 steps. Rapid cooling restricts exploration; very slow cooling can consume the budget before sufficient exploitation. Local Beam Search with k = 3 evaluates 15 successors per iteration, making it more costly for the same iteration count. The observations are individual stochastic runs, so they do not establish that slow cooling always yields a better result.')
paragraph('GitHub: https://github.com/ashenbandara02/IT3012---Practical-Base')

def footer(canvas, doc):
    canvas.setFont('Helvetica', 8)
    canvas.drawString(36, 22, 'IT24100315 | Lab 05')
    canvas.drawRightString(559, 22, str(doc.page))

SimpleDocTemplate(str(ROOT / 'IT24100315_LAB05_COMPLETED.pdf'),
                  rightMargin=36, leftMargin=36, topMargin=36,
                  bottomMargin=36).build(story, onFirstPage=footer, onLaterPages=footer)
print('Exported IT24100315_LAB05_COMPLETED.pdf')
