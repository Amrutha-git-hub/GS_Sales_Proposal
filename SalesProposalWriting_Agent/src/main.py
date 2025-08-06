from SalesProposalWriting_Agent.src.agent import graph
from SalesProposalWriting_Agent.src.states import State
from WebScraper.state import User
from SalesProposalWriting_Agent.src.sales_proposal_html_writing import generate_modern_presentation
from SalesProposalWriting_Agent.src.utils import  *
from dotenv import load_dotenv
load_dotenv()
import os 
import pdfkit
from weasyprint import HTML, CSS
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import tempfile
import logging
import warnings

# Suppress the BeautifulSoup warning
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

OUTPUT_FILE_DIRECTORY = os.getenv("OUTPUT_PATH")

def find_file_path(filename: str, search_dir: str = ".") -> str:
    for root, dirs, files in os.walk(search_dir):
        if filename in files:
            return os.path.abspath(os.path.join(root, filename))
    return None 

def get_presentation(client, seller, project_specs, output_format='html'):
    """
    Enhanced function to generate both HTML and PDF presentations
    
    Args:
        client: Client data
        seller: Seller data
        project_specs: Project specifications
        output_format: 'html', 'pdf', or 'both' (default: 'both')
    
    Returns:
        tuple: (html_content, html_file_path, pdf_file_path) or (html_content, html_file_path) if PDF not requested
    """
    
    # Initialize state and generate HTML content
    state = State(client=client, seller=seller, project_specs=project_specs, sections=[], final_result='')
    
    client_logo = client.enterprise_logo
    seller_logo = seller.enterprise_logo
    
    # Setup directories with proper path handling
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    proposals_dir = os.path.join(project_root, "SalesProposalsGenerated_txt_and_html")
    
    # Create directory if it doesn't exist
    try:
        os.makedirs(proposals_dir, exist_ok=True)
        print(f"Created/verified directory: {proposals_dir}")
    except Exception as e:
        print(f"Error creating directory {proposals_dir}: {e}")
        # Fallback to current directory
        proposals_dir = os.getcwd()
        print(f"Using fallback directory: {proposals_dir}")
    
    # Generate base filename
    base_filename = "benori"
    
    # Generate HTML content
    txt_file_path = os.path.join(proposals_dir, f"{base_filename}.txt")
    print("Starting HTML generation...")
    
    try:
        html_content, html_file_path = generate_modern_presentation(
            filename=txt_file_path,
            logo_url=client_logo,
            logo_url_2=seller_logo
        )
        print("HTML generation completed")
    except Exception as e:
        print(f"Error generating HTML: {e}")
        return None, None, None
    
    # Generate PDF if requested
    pdf_file_path = None
    if output_format in ['pdf', 'both']:
        try:
            pdf_file_path = generate_pdf_from_html(html_content, proposals_dir, base_filename)
        except Exception as e:
            print(f"PDF generation failed: {e}")
            pdf_file_path = None
    
    if output_format == 'html':
        return html_content, html_file_path
    elif output_format == 'pdf':
        return html_content, html_file_path, pdf_file_path
    else:  # 'both'
        return html_content, html_file_path, pdf_file_path

def generate_pdf_from_html(html_content, output_dir, base_filename):
    """
    Generate PDF from HTML content using multiple fallback methods
    
    Args:
        html_content: HTML content string
        output_dir: Output directory for PDF
        base_filename: Base filename for the PDF
    
    Returns:
        str: Path to generated PDF file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_file_path = os.path.join(output_dir, f"{base_filename}.pdf")
    print(f"Target PDF path: {pdf_file_path}")
    
    # Validate HTML content
    if not html_content or not isinstance(html_content, str):
        raise ValueError("Invalid HTML content provided")
    
    # Method 1: Try WeasyPrint (recommended for complex HTML/CSS)
    try:
        print("Attempting PDF generation with WeasyPrint...")
        
        # Clean HTML for better PDF rendering
        cleaned_html = clean_html_for_pdf(html_content)
        
        # Create a temporary HTML file to avoid path issues
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
            temp_html.write(cleaned_html)
            temp_html_path = temp_html.name
        
        try:
            # Generate PDF with WeasyPrint
            HTML(filename=temp_html_path).write_pdf(
                pdf_file_path,
                stylesheets=[CSS(string=get_pdf_css())]
            )
            
            print(f"PDF generated successfully with WeasyPrint: {pdf_file_path}")
            return pdf_file_path
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_html_path)
            except:
                pass
        
    except Exception as e:
        print(f"WeasyPrint failed: {str(e)}")
        
        # Method 2: Try pdfkit (wkhtmltopdf wrapper)
        try:
            print("Attempting PDF generation with pdfkit...")
            
            # Check if wkhtmltopdf is available
            try:
                import subprocess
                subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("wkhtmltopdf not found. Please install wkhtmltopdf.")
                raise Exception("wkhtmltopdf not available")
            
            # Configure pdfkit options
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
                'disable-smart-shrinking': '',
                'print-media-type': '',
            }
            
            # Use temporary HTML file approach for pdfkit too
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
                temp_html.write(html_content)
                temp_html_path = temp_html.name
            
            try:
                pdfkit.from_file(temp_html_path, pdf_file_path, options=options)
                print(f"PDF generated successfully with pdfkit: {pdf_file_path}")
                return pdf_file_path
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_html_path)
                except:
                    pass
            
        except Exception as e:
            print(f"pdfkit failed: {str(e)}")
            
            # Method 3: Fallback - save HTML file with instructions
            try:
                print("Saving HTML file as fallback...")
                html_fallback_path = os.path.join(output_dir, f"{base_filename}_for_pdf_conversion.html")
                
                with open(html_fallback_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"HTML file saved: {html_fallback_path}")
                print("You can manually convert this HTML file to PDF using:")
                print("1. Your browser's Print to PDF function")
                print("2. Online HTML to PDF converters")
                print("3. Install wkhtmltopdf and try again")
                
                return html_fallback_path
                
            except Exception as e:
                print(f"HTML fallback failed: {str(e)}")
                raise Exception("All PDF generation methods failed")

def clean_html_for_pdf(html_content):
    """
    Clean and optimize HTML content for PDF generation
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove or replace problematic elements
        for script in soup.find_all('script'):
            script.decompose()
        
        # Handle CSS animations and transitions
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                style_content = style_tag.string
                # Remove CSS animations and transitions that don't work in PDF
                cleaned_style = style_content.replace('@keyframes', '/* @keyframes */')
                cleaned_style = cleaned_style.replace('animation:', '/* animation: */')
                cleaned_style = cleaned_style.replace('transition:', '/* transition: */')
                style_tag.string = cleaned_style
        
        # Ensure proper HTML structure
        if not soup.html:
            # Wrap content in html tag if missing
            html_tag = soup.new_tag('html')
            html_tag.extend(soup.contents)
            soup.clear()
            soup.append(html_tag)
        
        # Ensure head exists
        if not soup.head:
            head_tag = soup.new_tag('head')
            if soup.html:
                soup.html.insert(0, head_tag)
        
        # Ensure proper encoding
        if soup.head and not soup.head.find('meta', charset=True):
            meta_tag = soup.new_tag('meta', charset='utf-8')
            soup.head.insert(0, meta_tag)
        
        return str(soup)
        
    except Exception as e:
        print(f"Error cleaning HTML: {e}")
        # Return original content if cleaning fails
        return html_content

def get_pdf_css():
    """
    Return CSS optimized for PDF generation
    """
    return """
    @page {
        size: A4;
        margin: 0.75in;
    }
    
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        font-size: 12pt;
        margin: 0;
        padding: 0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        margin-top: 1em;
        margin-bottom: 0.5em;
        page-break-after: avoid;
    }
    
    h1 { font-size: 24pt; }
    h2 { font-size: 20pt; }
    h3 { font-size: 16pt; }
    h4 { font-size: 14pt; }
    h5 { font-size: 12pt; }
    h6 { font-size: 11pt; }
    
    p {
        margin-bottom: 1em;
        text-align: justify;
        orphans: 2;
        widows: 2;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1em;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
        vertical-align: top;
    }
    
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    
    .page-break {
        page-break-before: always;
    }
    
    .no-break {
        page-break-inside: avoid;
    }
    
    img {
        max-width: 100%;
        height: auto;
        page-break-inside: avoid;
    }
    
    .header {
        text-align: center;
        margin-bottom: 2em;
        padding-bottom: 1em;
        border-bottom: 2px solid #3498db;
    }
    
    .footer {
        margin-top: 2em;
        padding-top: 1em;
        border-top: 1px solid #ddd;
        font-size: 10pt;
        color: #666;
    }
    
    /* Remove problematic CSS that doesn't work in PDF */
    * {
        -webkit-print-color-adjust: exact !important;
        color-adjust: exact !important;
    }
    
    /* Ensure visibility */
    .hidden, .d-none {
        display: block !important;
        visibility: visible !important;
    }
    """

