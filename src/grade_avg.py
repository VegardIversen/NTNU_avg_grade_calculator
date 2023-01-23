import PyPDF2
import re
from statistics import mean



# Open the PDF file

def calc_avg_grade(path):
    '''
    Method for calculating the average grade of a student based on NTNU rules:
    1. Each letter grade is replaced by a numerical equivalent, A=5, B=4, C=3, D=2, E=1.

    2. The numerical equivalent is multiplied by the subject's credits, and the individual products of credits and numerical equivalent are summed for the subjects included.

    3. The product sum is divided by the total number of credits included in the collection of relevant subjects.

    4. The quotient is calculated to one decimal place.

    5. The average grade will be the letter grade that has the whole number in the quotient as a numerical equivalent, after the normal increase rule has been applied."

    The regulation is interpreted in the same way that FS calculates the average grade. We use rounding to whole numbers. For example, 3.45 must be calculated with only one decimal place, regardless of how many decimal places there are: 3.4 is rounded to 3. The answer is C on average.
    

    This is only tested for PDFs from "Vitnemålsportalen"
    '''
    num_grade_map = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1}
    letter_grade_map = {5: 'A', 4: 'B', 3: 'C', 2: 'D', 1: 'E'}
    grade_avg = 0
    num_grades = 0
    grades_and_credits = []
    with open(path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # Initialize an empty list to store the grades
        grades = []
        # Iterate through all the pages
        for page_num in range(len(pdf_reader.pages)):
            # Get the page
            page = pdf_reader.pages[page_num]
            # Extract the text from the page
            pdf_text = page.extract_text()
            # Iterate through the rows
            for row in pdf_text.split('\n'):
                match = re.search("stp(.*)", row)
                if match:
                    #print(row)
                    
                    
                    grade = match.group(1)
                    if grade in num_grade_map:
                        credit_match = re.search(r"(\d+,\d+|\d+)\sstp", row)
                        credit = float(credit_match.group(1).replace(',', '.'))
                        grade_avg += num_grade_map[grade]
                        num_grades += 1
                        grades.append(grade)
                        grades_and_credits.append((grade, credit))


        product_sum = 0
        total_credits = 0
        for grade, credits in grades_and_credits:
            numerical_equivalent = num_grade_map[grade]
            product_sum += numerical_equivalent * credits
            total_credits += credits

        # Calculate the average grade
        average_grade = round(product_sum / total_credits, 1)
        average_letter_grade = letter_grade_map[round(average_grade)]
        print(f'Average grade: {average_grade} ({average_letter_grade})')
        return average_grade, average_letter_grade
        

