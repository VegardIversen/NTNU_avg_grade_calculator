from src.grade_avg import calc_avg_grade
import argparse

def main():
    ''' 
    run this with the path to the pdf file to calculate the average grade. 
    
    '''
    #check if the path is valid
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the pdf file")
    args = parser.parse_args()
    path = args.path
    calc_avg_grade(path)


    

if __name__ == '__main__':
    main()