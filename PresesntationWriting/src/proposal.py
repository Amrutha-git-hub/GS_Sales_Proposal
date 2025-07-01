from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .llms import llm
from .states import State





p_template = '''You are a senior enterprise consultant and proposal strategist with years of experience writing persuasive, high-quality sales proposals for B2B companies across technology, digital, and marketing domains.

Your task is to generate a **structured, executive-grade Sales Proposal** based on the input below. Keep the tone professional and persuasive, suitable for leadership and decision-makers.

---

## 🧩 Client Organization:
{client_details}

## 🏢 Seller Organization:
{seller_details}


---

### 📄 Required Sections

Use the following sections in this exact order. Do **not create new sections**, and **do not rename them**. Keep most sections **concise (2–4 paragraphs)** but make **“Scope of Work” very detailed** with structured breakdowns.

{section_list}

At the end, always include:
- **Who We Are**
- **What We Do**

---

### 🛠️ Special Instructions for “Scope of Work”

This section must be written in **detailed breakdown format**.

- Use clear subheaders or bullet points for each phase or deliverable.
- Elaborate tasks clearly using context from additional informtation
-----------
{project_specs}.
----------------
IMPORTANT : If there is no breakdown of the task then breakdown yourself and then explain each phase with atleast 4-5 bullet points
and if there is breakdown then do try to utilize info and still write 4-5 points properly
- Example format:

Discovery & Planning (Week 1–2)

Conduct kickoff with buyer team to gather expectations

Create user journeys and goal mapping

Perform competitive audit for design inspiration and SEO alignment

UI/UX Design (Week 3–4)

Wireframes for key pages

Brand-aligned visual mockups with review cycles

Frontend Development (Week 5–7)

Responsive development using Bootstrap

Animations, product pages, and forms



Use **phase-wise structuring** like Discovery, Design, Development, Launch, SEO, etc., and explain each step in business-impact terms — showing **how it contributes to client goals**.

---

### ✍️ Writing Style & Examples

Follow these guidelines:

- ✅ Use a **professional, business-friendly tone** suitable for executive audiences.
- ✅ Write **2–4 paragraphs per section** — detailed, but not bloated.
- ✅ Use bullet points where appropriate (for Deliverables, Timelines, Fee Structure).
- ✅ Integrate contextually — refer to business goals, constraints, project scope, and domain.
- ✅ Emphasize **value, clarity, and confidence** — this is a persuasive sales proposal.

---

### 📤 Output Format

Return the final result as a list of dictionaries, each with `"title"` and `"text"` fields, in **valid JSON-like format**:

```json
[ {{"title":"Title of the proposal","text":"..."}}
  {{"title": "Executive Summary", "text": "..."}},
  {{"title": "Scope of Work", "text": "..."}},
  ...
  {{"title": "Who We Are", "text": "..."}},
  {{"title": "What We Do", "text": "..."}}
]

'''

# Set up LangChain prompt + parser
p_prompt = ChatPromptTemplate.from_template(p_template)
p_chain = p_prompt | llm | StrOutputParser()

# Function to generate the full proposal
def write_sales_proposal(state:State):
    section_string = "\n".join([f"- {s}" for s in state.sections])

    result = p_chain.invoke({
        'client_details':state.client,
        'seller_details':state.seller,
        'project_specs':state.project_specs,
        'section_list':section_string

    })

    return {'final_result': result}
