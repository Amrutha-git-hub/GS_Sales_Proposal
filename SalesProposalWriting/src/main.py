from SalesProposalWriting.src.agent import graph
from SalesProposalWriting.src.states import State
from WebScraper.state import User
from SalesProposalWriting.src.sales_proposal_html_writing import generate_modern_presentation
from SalesProposalWriting.src.utils import  *
from dotenv import load_dotenv
load_dotenv()
import os 
OUTPUT_FILE_DIRECTORY = os.getenv("OUTPUT_PATH")



#-------------------- These are used previously as default for testing not used anymore-----------------------------------------------------

# buyer = User(name='Benori Knowledge' , logo='https://benori.com/assets/web/images/Benori_Logo.svg' ,description='Benori is a trusted partner for custom research and analytics solutions for our clients globally, empowering them with key insights needed to drive intelligent decision-making and accelerate growth.' ,services=['Custom research and analytics solutions'])
# seller = User(name='GROWTHSUTRA LLP', logo='https://static.wixstatic.com/media/cb6b3d_5c8f2b020ebe48b69bc8c163cc480156~mv2.png/v1/fill/w_60,h_60,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/GrowthSutra%20Logo.png', description="At GrowthSutra, we are the go-to experts dedicated to accelerate brand and revenue growth for startups and SMBs. We provide the Fortune 500-caliber strategic thinking and flawless execution needed to gain market access, customer traction, and investor interest. Our team is comprised of seasoned marketing, communications, sales, and leadership executives, each with over 20+ years of real-world expertise launching and scaling disruptive brands across technology, e-commerce, climate, FMCG, and other major industries. We combine our team's unmatched experience with rigorous project governance and proven data-driven frameworks to get you measurable results fast. Our approach is tailored to each client's unique needs and objectives.", services=['Go-To-Market Partner', 'On-Demand CMO', 'Revenue Architect', 'XPRT Co-Pilots', 'B2B Revenue Engine Design', 'Sales Enablement Audit', 'RevenueOps Audit'])
# client_requirement = '''Increasing sales by 10% within a year 

#     *   **Anticipate and Acknowledge Pain Points:** Identify potential challenges or concerns the client might have regarding the project (e.g., budget constraints, tight deadlines, integration complexities).
#     *   **Offer Mitigation Strategies:** For each identified pain point, propose concrete solutions or mitigation strategies. This demonstrates foresight and a commitment to problem-solving.
#     *   **Address Risk Management:** Include a section on risk management, outlining potential risks and the steps you will take to minimize their impact.
#     *   **Offer Flexible Options:** Where possible, provide flexible options to accommodate potential client constraints. This could include phased implementation, customizable solutions, or alternative pricing models.
#     *   **Provide Clear Communication Plan:** Outline how you will maintain communication throughout the project, ensuring transparency and addressing concerns promptly.
    

#     *   **Clearly Define Project Objectives:** Collaboratively define the specific, measurable, achievable, relevant, and time-bound (SMART) objectives of the project. Ensure these align with the client's broader strategic goals.
#     *   **Demonstrate Understanding of Client's Industry:** Research and demonstrate a deep understanding of the client's industry, competitive landscape, and market trends.
#     *   **Showcase Long-Term Value:** Emphasize the long-term benefits of the proposed solution, such as increased efficiency, improved profitability, or enhanced market position.
#     *   **Propose Metrics for Success:** Define key performance indicators (KPIs) that will be used to measure the success of the project and track progress toward achieving the client's goals.
#     *   **Offer Scalability and Future-Proofing:** Demonstrate how the proposed solution can be scaled or adapted to meet the client's future needs and evolving business environment.
    

#     *   **Highlight Key Differentiators:** Emphasize what makes your company unique compared to competitors. This could be proprietary technology, a specialized team, or a proven methodology. Tailor these differentiators to align with potential client needs.
#     *   **Present Compelling Case Studies:** Include relevant case studies that demonstrate successful outcomes achieved for similar clients or projects. Quantify the results (e.g., cost savings, revenue increase, efficiency gains) to showcase tangible value.
#     *   **Offer a Focused Service Portfolio:** Rather than overwhelming the client with every service, highlight the core offerings that directly address their likely needs. Position these as the cornerstone of the proposed solution.
#     *   **Introduce the Expert Team:** Briefly introduce key personnel who will be working on the project, highlighting their relevant experience and qualifications. This builds trust and demonstrates competence.
#     *   **Provide a Clear Process Overview:** Outline the steps involved in delivering the core services, providing transparency and demonstrating a well-defined approach. This shows that you have a reliable, repeatable process.
    
# '''

# additonal_info = ['''
#   • Phase 1: Discovery & Strategy (5 days)
#     - Team: 2 Project Managers, 1 Marketing Analyst
#     - Tasks: Market research, competitor analysis, target audience identification, objective definition, KPI establishment.
#     - Cost: $25,000

#   • Phase 2: Content & Creative Development (10 days)
#     - Team: 2 Content Writers, 2 Graphic Designers
#     - Tasks: Content creation (website, blog, social media), visual asset design (ads, infographics).
#     - Cost: $50,000

#   • Phase 3: Campaign Execution & Management (10 days)
#     - Team: 2 Digital Marketing Specialists, 1 Data Analyst
#     - Tasks: Campaign setup, ad buying, social media management, performance monitoring, A/B testing.
#     - Cost: $50,000

#   • Phase 4: Analysis & Reporting (5 days)
#     - Team: 1 Data Analyst, 1 Project Manager
#     - Tasks: Data analysis, report generation, insights and recommendations for future campaigns.
#     - Cost: $25,000
#   ''']

# service_dept = ['Go-To-Market Partner', 'On-Demand CMO']


# final_result = ''


# state = State(buyer=buyer , seller = seller , client_requirement=client_requirement,additional_info=additonal_info,service_dept=service_dept,sections=[],final_result=final_result)

# state = graph.invoke(state)

# print(state)

# logo = state['seller'].logo
# colors = get_color_from_image(logo)
# print(colors)
# generate_presentation(filename  = 'output.txt',logo_url=logo,colors = colors,output_format='pdf')
# generate_presentation(filename='output.txt',logo_url = logo,colors=colors,output_format='html')
# def parse_to_user(data_str: str) -> User:
#     # Convert the multiline assignment string into a dictionary
#     lines = [line.strip() for line in data_str.strip().splitlines()]
#     data_dict = {}
#     for line in lines:
#         key, value = line.split('=', 1)
#         data_dict[key.strip()] = ast.literal_eval(value.strip())
    
#     # Create a User instance
#     return User(**data_dict)



def get_presentation(client , seller , project_specs ):
    # buyer = parse_to_user(buyer)
    # seller = parse_to_user(seller)
    #print(type(buyer),buyer)
    state = State(client = client , seller=seller , project_specs=project_specs,sections=[],final_result='')
    # state = graph.invoke(state)
    # colors = [ '#4F4F4F', '#101213', '#DBDBDB', '#299E75']

    client_logo = client.enterprise_logo
    seller_logo = seller.enterprise_logo
    # target = os.path.join(OUTPUT_FILE_DIRECTORY,client.enterprise_name)
    # file_path = os.path.join(target,"salesproposal.txt")
    # print(f"_______________________________________________File path is {file_path}")
    file_path = '/home/shreyank/GS/GS_Sales_Proposal/SalesProposalsGenerated/benori.txt'
    print("F--------------------Starting in main")
    html_content,html_file_name = generate_modern_presentation(filename  = file_path ,logo_url=client_logo,logo_url_2 = seller_logo )
    print("F--------------------Ending in main")
    return html_content,html_file_name


