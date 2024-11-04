from fpdf import FPDF

def create_menu_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "Joe's Restaurant Menu", ln=True, align='C')
    
    # Appetizers
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "Appetizers", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "1. Garlic Bread - $5.99", ln=True)
    pdf.cell(0, 10, "2. Caesar Salad - $8.99", ln=True)
    pdf.cell(0, 10, "3. Soup of the Day - $6.99", ln=True)
    
    # Main Courses
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "Main Courses", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "1. Grilled Salmon - $24.99", ln=True)
    pdf.cell(0, 10, "2. Beef Tenderloin - $29.99", ln=True)
    pdf.cell(0, 10, "3. Vegetarian Pasta - $18.99", ln=True)
    
    # Desserts
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "Desserts", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "1. Chocolate Cake - $7.99", ln=True)
    pdf.cell(0, 10, "2. Ice Cream Sundae - $6.99", ln=True)
    pdf.cell(0, 10, "3. Apple Pie - $7.99", ln=True)
    
    pdf.output("../assets/menu.pdf")

if __name__ == "__main__":
    create_menu_pdf() 