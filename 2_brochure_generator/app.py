import streamlit as st
import subprocess
import markdown
from playwright.sync_api import sync_playwright

from services.model_service import ModelService


# ----------------------------
# Streamlit config
# ----------------------------
st.set_page_config(
    page_title="AI Brochure Generator",
    page_icon="📄",
    layout="wide"
)


# ----------------------------
# Ensure Playwright Chromium is installed
# ----------------------------
@st.cache_resource
def install_browser():
    subprocess.run(["playwright", "install", "chromium"], check=True)
    subprocess.run(["playwright", "install-deps", "chromium"], check=True)


install_browser()


# ----------------------------
# Cache model service
# ----------------------------
@st.cache_resource
def get_model_service():
    return ModelService()


# ----------------------------
# Markdown → PDF using Playwright
# ----------------------------
def markdown_to_pdf(company_name: str, markdown_text: str) -> bytes:
    md = markdown_text.strip()

    if not md.startswith("# "):
        md = f"# {company_name}\n\n{md}"

    html_body = markdown.markdown(
        md,
        extensions=["extra", "tables", "fenced_code"]
    )

    html = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: "Cormorant Garamond", "Playfair Display", Georgia, serif;
                    margin: 15px;
                    color: #141414;
                    line-height: 1.85;
                    font-size: 16.5px;
                    letter-spacing: 0.2px;
                    background: #ffffff;
                }}

                h1, h2, h3 {{
                    font-family: "Playfair Display", "Didot", serif;
                    font-weight: 500;
                    letter-spacing: 1.2px;
                    color: #0f0f0f;
                    margin-bottom: 18px;
                }}

                p {{
                    font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
                    font-size: 15.5px;
                    line-height: 1.9;
                    color: #2a2a2a;
                    margin-bottom: 14px;
                }}

                ul {{
                    margin-left: 28px;
                    padding-left: 0;
                    list-style-type: "• ";
                    color: #1f1f1f;
                }}

                li {{
                    margin-bottom: 8px;
                    line-height: 1.8;
                    font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
                }}

               table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 18px;
                    margin-bottom: 18px;
                    font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
                    font-size: 14.5px;
                    color: #1a1a1a;
                }}

                th {{
                    text-align: left;
                    font-weight: 500;
                    padding: 12px 10px;
                    border-bottom: 1px solid #e6e6e6;
                    letter-spacing: 0.5px;
                }}

                td {{
                    padding: 12px 10px;
                    border-bottom: 1px solid #f0f0f0;
                }}

                tr:hover {{
                    background-color: #fafafa;
                }}

                blockquote {{
                    border-left: 2px solid #b89b5e;
                    padding: 14px 18px;
                    margin: 24px 0;
                    color: #444;
                    font-style: italic;
                    font-family: "Cormorant Garamond", "Georgia", serif;
                    background: #faf9f7;
                }}
            </style>
        </head>

        <body>
            {html_body}
        </body>
    </html>
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )
        page = browser.new_page()

        page.set_content(html, wait_until="load")

        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={
                "top": "20mm",
                "bottom": "20mm",
                "left": "15mm",
                "right": "15mm"
            }
        )

        browser.close()

        return pdf_bytes


# ----------------------------
# UI
# ----------------------------
def main():
    st.title("📄 AI Brochure Generator")

    st.markdown(
        "Generate a professional brochure by analyzing a company's website and relevant pages."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Company Name", placeholder="e.g. OpenAI")

    with col2:
        website_url = st.text_input(
            "Company Website", placeholder="https://openai.com")

    st.divider()

    # ----------------------------
    # Generate brochure
    # ----------------------------
    if st.button("Generate Brochure", type="primary", use_container_width=True):

        if not company_name.strip():
            st.error("Please enter a company name")
            return

        if not website_url.strip():
            st.error("Please enter a website URL")
            return

        try:
            model_service = get_model_service()

            with st.spinner("Generating brochure..."):
                st.session_state["brochure_markdown"] = (
                    model_service.get_brochure_markdown(
                        company_name,
                        website_url
                    )
                )

            st.success("Brochure generated!")

        except Exception as ex:
            st.error(f"Failed to generate brochure: {str(ex)}")
            return

    # ----------------------------
    # Preview (persisted)
    # ----------------------------
    if "brochure_markdown" in st.session_state:
        st.subheader("Preview")
        st.markdown(st.session_state["brochure_markdown"])

        # ----------------------------
        # Generate PDF only if markdown exists
        # ----------------------------
        try:
            with st.spinner("Generating PDF (Chromium)..."):
                pdf_bytes = markdown_to_pdf(
                    company_name,
                    st.session_state["brochure_markdown"]
                )

            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"{company_name.lower().replace(' ', '_')}_brochure.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as ex:
            st.error(f"PDF generation failed: {str(ex)}")


if __name__ == "__main__":
    main()
