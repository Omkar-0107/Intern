import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import tempfile
from PIL import Image as PILImage

# Function to generate PDF
def generate_pdf(name, email, phone, education, experience, skills, photo_path=None):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        doc = SimpleDocTemplate(tmpfile.name, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            name='TitleStyle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=14,
            alignment=1  # Center alignment
        )
        
        subtitle_style = styles['Heading2']
        subtitle_style.fontSize = 18
        subtitle_style.spaceAfter = 12
        
        body_style = styles['BodyText']
        body_style.fontSize = 12
        body_style.leading = 14
        
        elements = []

        # Add Title
        elements.append(Paragraph(f"{name}'s Resume", title_style))
        elements.append(Spacer(1, 12))

        # Add Photo if provided
        if photo_path:
            elements.append(Image(photo_path, width=1.5*inch, height=1.5*inch))
            elements.append(Spacer(1, 12))

        # Add contact info
        contact_info = f"<b>Email:</b> {email}<br/><b>Phone:</b> {phone}"
        elements.append(Paragraph(contact_info, body_style))
        elements.append(Spacer(1, 12))

        # Add sections
        def add_section(title, content):
            elements.append(Paragraph(title, subtitle_style))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(content.replace('\n', '<br/>'), body_style))
            elements.append(Spacer(1, 12))

        add_section("Education", education)
        add_section("Experience", experience)
        add_section("Skills", skills)

        # Build PDF
        doc.build(elements)
        return tmpfile.name

# Streamlit app
def main():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://wallpapers.com/images/hd/professional-background-53kprhryuo5bszds.jpg");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Resume Maker")

    # Form to input resume data
    with st.form(key='resume_form'):
        name = st.text_input("Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        education = st.text_input("Education")
        experience = st.text_input("Experience")
        skills = st.text_input("Skills")
        photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button(label='Create Resume')

    # Generate and display PDF
    if submit_button:
        if not phone.isdigit() or len(phone) != 10:
            st.error("Phone number must be exactly 10 digits.")
        else:
            photo_path = None
            if photo:
                photo_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                img = PILImage.open(photo)
                img.save(photo_path)

            pdf_file = generate_pdf(name, email, phone, education, experience, skills, photo_path)
            with open(pdf_file, "rb") as f:
                pdf_data = f.read()
            st.download_button(label="Download Resume PDF", data=pdf_data, file_name="resume.pdf", mime="application/pdf")

if __name__ == '__main__':
    main()
