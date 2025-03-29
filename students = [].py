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

def add_student():
    """한 명의 학생 정보를 입력받아 추가"""
    student_id = input("학번: ")
    name = input("이름: ")
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

def input_students():
    """5명의 학생 정보를 입력받음"""
    for _ in range(5):
        add_student()

def calculate_rank():
    """총점 기준으로 등수를 계산 (동점자 고려)"""
    students.sort(key=lambda x: x["총점"], reverse=True)
    rank = 1
    prev_total = None
    for i, student in enumerate(students):
        if prev_total is not None and student["총점"] == prev_total:
            student["등수"] = rank  # 동점자 처리
        else:
            rank = i + 1
            student["등수"] = rank
        prev_total = student["총점"]

def print_results():
    """학생 정보를 출력"""
    if not students:
        print("\n학생 정보가 없습니다.")
        return
    
    print("\n" + " 성적관리 프로그램 ".center(80, "="))
    print("=" * 100)
    print(f"{'학번':<15}{'이름':<10}{'영어':<8}{'C-언어':<8}{'파이썬':<8}{'총점':<8}{'평균':<8}{'학점':<6}{'등수':<6}")
    print("=" * 100)

    for student in students:
        print(f"{student['학번']:<15}{student['이름']:<10}{student['영어']:<8}{student['C-언어']:<8}"
              f"{student['파이썬']:<8}{student['총점']:<8}{student['평균']:<8.2f}{student['학점']:<6}{student['등수']:<6}")

def search_student():
    """학번 또는 이름으로 학생 검색"""
    key = input("검색할 학번 또는 이름 입력: ")
    found = False
    for student in students:
        if student["학번"] == key or student["이름"] == key:
            print("\n검색 결과:")
            print("=" * 60)
            print(f"학번: {student['학번']}, 이름: {student['이름']}, 총점: {student['총점']}, 평균: {student['평균']:.2f}, 학점: {student['학점']}, 등수: {student['등수']}")
            found = True
    if not found:
        print("\n해당하는 학생을 찾을 수 없습니다.")

def delete_student():
    """학번을 입력받아 학생 삭제"""
    student_id = input("삭제할 학생의 학번 입력: ")
    global students
    students = [student for student in students if student["학번"] != student_id]
    print(f"\n학번 {student_id} 학생이 삭제되었습니다.")
    calculate_rank()  # 삭제 후 등수 재계산

def sort_students():
    """총점 기준 정렬"""
    students.sort(key=lambda x: x["총점"], reverse=True)
    print("\n총점 기준 정렬 완료.")

def count_above_80():
    """80점 이상인 학생 수 계산"""
    count = sum(1 for student in students if student["평균"] >= 80)
    print(f"\n80점 이상 학생 수: {count}명")

def main():
    """메뉴 기반 실행"""
    while True:
        print("\n메뉴")
        print("1. 학생 입력")
        print("2. 학생 출력")
        print("3. 학생 추가")
        print("4. 학생 삭제")
        print("5. 학생 검색")
        print("6. 총점 기준 정렬")
        print("7. 80점 이상 학생 수 출력")
        print("0. 종료")
        choice = input("선택: ")

        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        elif choice == "1":
            input_students()
            calculate_rank()
        elif choice == "2":
            print_results()
        elif choice == "3":
            add_student()
            calculate_rank()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            search_student()
        elif choice == "6":
            sort_students()
        elif choice == "7":
            count_above_80()
        else:
            print("잘못된 입력입니다. 다시 선택하세요.")

if __name__ == "__main__":
    main()
