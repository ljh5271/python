
students = []
def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 85:
        return "B+"
    elif avg >= 80:
        return "B"
    elif avg >= 75:
        return "C+"
    elif avg >= 70:
        return "C"
    elif avg >= 65:
        return "D+"
    elif avg >= 60:
        return "D"
    else:
        return "F"

def input_student():
   for i in range(5):
    student_id = input("학번: ")
    name = input("학생이름: ") 
    english = int(input("영어 점수: "))
    c_language = int(input("C-언어 점수: "))
    python = int(input("파이썬 점수: "))


    total = english + c_language + python
    avg = total / 3
    grade = calculate_grade(avg)

    
    students.append({
            "학번": student_id,
            "이름": name,
            "영어": english,
            "C-언어": c_language,
            "파이썬": python,
            "총점": total,
            "평균": avg,
            "학점": grade,
            "등수": 0  
        })

def calculate_rank():
    students.sort(key=lambda x: x["총점"], reverse=True)  
    for i, student in enumerate(students):
        student["등수"] = i + 1  


def print_results():
    print("\n" + "성적관리 프로그램".center(80))
    print("=" * 100)
    print(f"{'학번':<15}{'이름':<10}{'영어':<8}{'C-언어':<8}{'파이썬':<8}{'총점':<8}{'평균':<8}{'학점':<6}{'등수':<6}")
    print("=" * 100)

    for student in students:
        print(f"{student['학번']:<15}{student['이름']:<10}{student['영어']:<8}{student['C-언어']:<8}"
              f"{student['파이썬']:<8}{student['총점']:<8}{student['평균']:<8.2f}{student['학점']:<6}{student['등수']:<6}")


input_student()
calculate_rank()
print_results()