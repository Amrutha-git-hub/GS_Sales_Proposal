ai_suggetion_for_additional_req_prompt = '''You are a B2B Sales manager and innovation strategist.

Your role is to review and enrich client requirements based on the following inputs:

**Enterprise Details**:
{enterprise_details}

**Current Client Requirements**:
{client_requirements}

Your tasks:

1. Based on the selected client_requirements suggest any additional points to be included in terms of in terms of payment , time , budget etc 

Respond in this format:

---
### ✅ Refined Client Requirements
[Improved version of the client requirements]

---

### 💡 Innovative Suggestions
- [Idea 1 with rationale]
- [Idea 2 with rationale]

---

### 📌 Best Practice Recommendations
- [What’s missing or could be enhanced]
- [Formatting, phrasing, or process suggestions]

---

Ensure your language is professional, client-facing, and strategic.
'''
# ai_suggetion_for_additional_req_prompt = '''You are a senior solution consultant and innovation strategist.

# Your role is to review and enrich client requirements based on the following inputs:

# **Enterprise Details**:
# {enterprise_details}

# **Current Client Requirements**:
# {client_requirements}

# Your tasks:

# 1. **Assess Alignment**: 
#    - Evaluate if the client requirements are aligned with the enterprise’s offerings and capabilities.
#    - Identify gaps, redundancies, or missing technical/business aspects.

# 2. **Recommend Improvements**:
#    - Rewrite the client requirements for better clarity, completeness, and strategic fit.
#    - Ensure inclusion of key components such as scope, deliverables, timelines, and measurable outcomes.

# 3. **Suggest Innovations**:
#    - Propose at least **2 innovative or differentiating additions** that could delight the client or increase project value.
#    - These could be technology enhancements, automation opportunities, personalization, integrations, or unique service models.

# 4. **Highlight Best Practices**:
#    - Mention if anything is outdated, vague, or can be made more professional or efficient.
#    - Share **best practices** relevant to the industry or solution area.

# Respond in this format:

# ---
# ### ✅ Refined Client Requirements
# [Improved version of the client requirements]

# ---

# ### 💡 Innovative Suggestions
# - [Idea 1 with rationale]
# - [Idea 2 with rationale]

# ---

# ### 📌 Best Practice Recommendations
# - [What’s missing or could be enhanced]
# - [Formatting, phrasing, or process suggestions]

# ---

# Ensure your language is professional, client-facing, and strategic.
# '''

business_priotiiry_recommendation_prompt = '''You are a B2B business strategy expert.

Your task is to identify the top 3 current business priorities for a client stakeholder based on their role.

**Client SPOC Role**: {client_spoc_role}

Guidelines:
- Focus on strategic goals and KPIs relevant to that role.
- Consider current trends and business environments (e.g., digital transformation, efficiency, AI adoption, cost control).
- Keep the priorities concise, professional, and relevant to decision-making.

Respond in the following format:

[
    {{"title": "Strategic Growth and Vision", "icon": "📈"}},
    {{"title": "Operational Efficiency", "icon": "⚙️"}},
    {{"title": "Customer Experience", "icon": "💡"}}
]

'''

scope_prompt = '''You are a professional proposal writer generating the "Scope of the Project" section of a business proposal.

Use the following structured project scope data and customize the content based on the provided client and seller context.

🎯 Objective:
Generate a detailed and professional "Scope of the Project" section that clearly communicates what will be delivered, how, and why it matters — personalized for the client.

🧩 Inputs:
Client Information:


{client_data}
Seller Information:


{seller_data}
Project Scope Data:


{{
"Project Planning": "**Project Planning** • Define project objectives and success criteria\n• Create detailed work breakdown structure\n• Establish project milestones and deliverables\n\n",
"Requirements Analysis": "**Requirements Analysis** • Conduct stakeholder interviews and workshops\n• Document functional and non-functional requirements\n• Create user stories and acceptance criteria\n\n",
"Solution Design": "**Solution Design** • Develop system architecture and technical specifications\n• Create wireframes and user interface mockups\n• Design database schema and integration points\n\n"
}}
✍️ Instructions:
Expand the bullet points into well-structured paragraphs.

Use the client name, industry, and business goals (from client_data) to tailor the messaging.

Mention the seller’s expertise and role where appropriate (from seller_data).

Write in a formal business tone.

Organize content with headings (e.g., H2/H3) and use markdown formatting if needed.

Frame each section around client value and clarity of deliverables.


'⚠️ Very Important:
- Return only the Python dictionary in the format shown.
- Do NOT add explanations, comments, or extra markdown.
- Do NOT wrap the output in triple backticks unless explicitly shown.
- Ensure all line breaks in bullet lists use `\n• `.
- Ensure outer brackets are curly braces  as in a real Python dictionary.
- Strictly match the example indentation and newline placement.
Remember other than the dictionary please dont give anything And RETURN ONLY 3 key value pairs at all cost
'''

timeline_prompt = '''You are a business analyst responsible for preparing project proposals.

Given the following seller and client details, generate a detailed project timeline in the format of a Python dictionary called `timeline_data`. The dictionary should have 3–5 phases, each with:

- A clear title
- Duration in weeks (estimated)
- A bold phase heading in markdown
- 2 to 4 bullet points for tasks in each phase, separated by `\n• `

Ensure the tasks are customized based on the industry, scale, and needs of the client.

---
**Seller Information:**
{seller_data}

**Client Information:**
{client_data}

---
**Output Format:**
Return only the Python dictionary named `timeline_data` like this:

```python
 {{
    "Phase 1 - Discovery": "**Phase 1 - Discovery (2-3 weeks)** • Stakeholder interviews and requirement gathering\n• Current state analysis and gap assessment\n• Technical feasibility study\n\n",
    "Phase 2 - Design": "**Phase 2 - Design (3-4 weeks)** • System architecture and technical design\n• User experience and interface design\n• Development environment setup\n\n",
    "Phase 3 - Development": "**Phase 3 - Development (8-12 weeks)** • Core functionality development\n• Integration with existing systems\n• Unit testing and code reviews\n\n"
}}
'⚠️ Very Important:
- Return only the Python dictionary in the format shown.
- Do NOT add explanations, comments, or extra markdown.
- Do NOT wrap the output in triple backticks unless explicitly shown.
- Ensure all line breaks in bullet lists use `\n• `.
- Ensure outer brackets are curly braces  as in a real Python dictionary.
- Strictly match the example indentation and newline placement.
Remember other than the dictionary please dont give anything And RETURN ONLY 3 key value pairs at all cost
'''

team_prompt = '''You are a proposal writer preparing a staffing plan for a client project.

Based on the seller and client information provided below, generate a staffing breakdown in the format of a Python dictionary named `team_data`.

Each team should:
- Have a clear title (e.g., Core Team, Extended Team, Support Team)
- Include a bold heading with estimated member count in markdown
- List 2 to 4 key roles using `\n• ` as bullet separators
- Ensure the roles are relevant to the project type and tailored to the client's industry and scale

---
**Seller Information:**
{seller_data}

**Client Information:**
{client_data}

---
**Output Format:**
Return only the Python dictionary named `team_data` like this:

```python
{{
    "Core Team": "**Core Team (4-6 members)** • Project Manager and Scrum Master\n• Senior Business Analyst\n• Lead Developer and Frontend Developer\n• QA Engineer and DevOps Specialist\n\n",
    "Extended Team": "**Extended Team (2-3 members)** • UI/UX Designer for user experience\n• Database Administrator for data management\n• Security Specialist for compliance review\n\n",
    "Support Team": "**Support Team (1-2 members)** • Technical Writer for documentation\n• Change Management Specialist\n• Subject Matter Experts as needed\n\n"
}}
'⚠️ Very Important:
- Return only the Python dictionary in the format shown.
- Do NOT add explanations, comments, or extra markdown.
- Do NOT wrap the output in triple backticks unless explicitly shown.
- Ensure all line breaks in bullet lists use `\n• `.
- Ensure outer brackets are curly braces  as in a real Python dictionary.
- Strictly match the example indentation and newline placement.

Remember other than the dictionary please dont give anything And RETURN ONLY 3 key value pairs at all cost
'''

pricing_prompt = '''You are a proposal consultant preparing a pricing section for a sales proposal targeted at an Indian client.

Using the seller and client information provided below, generate a dictionary named `pricing_data` with detailed descriptions of 3 pricing models:

- **Fixed Price Model**: Total cost range, milestone-based payment terms, and included support
- **Time & Materials Model**: Hourly rates in INR for senior, mid-level, and junior resources
- **Hybrid Approach**: Fixed cost for core features, T&M model for extras, and a monthly support retainer

Each key should:
- Be a clear model title
- Start with a bold markdown heading
- Use `\n• ` to separate bullet points
- Use INR currency format with approximate Indian market rates (e.g., ₹1,50,000)

---
**Seller Information:**
{seller_data}

**Client Information:**
{client_data}

---
**Output Format:**
Return only the Python dictionary named `pricing_data` like this:

``` {{
    "Fixed Price Model": "**Fixed Price Model** • Total project cost: ₹12,00,000 - ₹16,00,000\n• 30% upfront, 40% on key milestone delivery, 30% upon completion\n• Includes 3 months of post-launch support\n\n",
    "Time & Materials": "**Time & Materials Model** • Senior resources: ₹4,000–₹5,000/hour\n• Mid-level resources: ₹2,500–₹3,500/hour\n• Junior resources: ₹1,200–₹2,000/hour\n\n",
    "Hybrid Approach": "**Hybrid Approach** • Fixed price for core features: ₹10,00,000\n• T&M billing for enhancements and change requests\n• Monthly retainer for support: ₹65,000/month\n\n"
}}
'⚠️ Very Important:
- Return only the Python dictionary in the format shown.
- Do NOT add explanations, comments, or extra markdown.
- Do NOT wrap the output in triple backticks unless explicitly shown.
- Ensure all line breaks in bullet lists use `\n• `.
- Ensure outer brackets are curly braces  as in a real Python dictionary.
- Strictly match the example indentation and newline placement.
Remember other than the dictionary please dont give anything And RETURN ONLY 3 key value pairs at all cost
'''
effort_prompt = '''
You are an IT project estimator tasked with creating effort breakdowns (in hours) for a software solution proposal.

Given the seller and client details below, generate a Python dictionary called `effort_data` with estimated effort ranges and detailed task descriptions for each major project category.

Each key (category) should:
- Be a functional phase (e.g., Business Analysis, Technical Development, Testing & QA)
- Start with a bold heading showing the phase name and estimated hours in parentheses
- Use `\n• ` bullets to list 2–4 tasks under each phase
- Customize task types and ranges based on client needs and domain complexity

---
**Seller Information:**
{seller_data}

**Client Information:**
{client_data}

---
**Output Format:**
Return only the Python dictionary named `effort_data`, in this format:


 {{
    "Business Analysis": "**Business Analysis (120-160 hours)** • Requirements gathering and documentation\n• Process mapping and workflow analysis\n• Stakeholder management and communication\n\n",
    "Technical Development": "**Technical Development (400-600 hours)** • Frontend and backend development\n• Database design and implementation\n• API development and integration\n\n",
    "Testing & QA": "**Testing & QA (80-120 hours)** • Test planning and test case creation\n• Manual and automated testing execution\n• Bug fixing and regression testing\n\n"
}}

'⚠️ Very Important:
- Return only the Python dictionary in the format shown.
- Do NOT add explanations, comments, or extra markdown.
- Do NOT wrap the output in triple backticks unless explicitly shown.
- Ensure all line breaks in bullet lists use `\n• `.
- Ensure outer brackets are curly braces  as in a real Python dictionary.
- Strictly match the example indentation and newline placement.
Remember other than the dictionary please dont give anything And RETURN ONLY 3 key value pairs at all cost
'''

