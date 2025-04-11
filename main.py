##############################
# 프로그램명: 성적관리 프로그램 (객체지향 버전)
# 작성자: 컴퓨터공학과 / 홍길동
# 작성일: 2025-04-11
# 프로그램 설명:
#   - 5명의 학생 성적(영어, C-언어, 파이썬)을 입력받고
#     총점, 평균, 학점, 등수를 계산/출력/관리하는 프로그램
#   - 삽입, 삭제, 검색, 정렬, 통계 기능 포함
##############################

class Student:
    def __init__(self, student_id, name, english, c_language, python):
        self.student_id = student_id
        self.name = name
        self.english = english
        self.c_language = c_language
        self.python = python
        self.total = self.english + self.c_language + self.python
        self.average = self.total / 3
        self.grade = self.calculate_grade()
        self.rank = 0

    def calculate_grade(self):
        avg = self.average
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

    def display(self):
        return (f"{self.student_id:<15}{self.name:<10}{self.english:<8}"
                f"{self.c_language:<8}{self.python:<8}{self.total:<8}"
                f"{self.average:<8.2f}{self.grade:<6}{self.rank:<6}")

class GradeManager:
    def __init__(self):
        self.students = []

    def add_student(self):
        student_id = input("학번: ")
        name = input("이름: ")
        english = int(input("영어 점수: "))
        c_language = int(input("C-언어 점수: "))
        python = int(input("파이썬 점수: "))
        self.students.append(Student(student_id, name, english, c_language, python))
        self.calculate_ranks()

    def input_students(self, count=5):
        for _ in range(count):
            self.add_student()

    def calculate_ranks(self):
        sorted_students = sorted(self.students, key=lambda s: s.total, reverse=True)
        rank = 1
        prev_total = None
        for i, student in enumerate(sorted_students):
            if prev_total is not None and student.total == prev_total:
                student.rank = rank
            else:
                rank = i + 1
                student.rank = rank
            prev_total = student.total

    def print_results(self):
        if not self.students:
            print("\n학생 정보가 없습니다.")
            return

        print("\n" + " 성적관리 프로그램 ".center(80, "="))
        print("=" * 100)
        print(f"{'학번':<15}{'이름':<10}{'영어':<8}{'C-언어':<8}{'파이썬':<8}{'총점':<8}{'평균':<8}{'학점':<6}{'등수':<6}")
        print("=" * 100)

        for student in self.students:
            print(student.display())

    def delete_student(self):
        student_id = input("삭제할 학생의 학번 입력: ")
        original_len = len(self.students)
        self.students = [s for s in self.students if s.student_id != student_id]
        if len(self.students) < original_len:
            print(f"\n학번 {student_id} 학생이 삭제되었습니다.")
            self.calculate_ranks()
        else:
            print("해당 학번의 학생을 찾을 수 없습니다.")

    def search_student(self):
        key = input("검색할 학번 또는 이름 입력: ")
        found = False
        for student in self.students:
            if student.student_id == key or student.name == key:
                print("\n검색 결과:")
                print("=" * 60)
                print(f"학번: {student.student_id}, 이름: {student.name}, 총점: {student.total}, 평균: {student.average:.2f}, 학점: {student.grade}, 등수: {student.rank}")
                found = True
        if not found:
            print("해당 학생을 찾을 수 없습니다.")

    def sort_students_by_total(self):
        self.students.sort(key=lambda s: s.total, reverse=True)
        print("\n총점 기준 정렬 완료.")

    def count_above_80(self):
        count = sum(1 for s in self.students if s.average >= 80)
        print(f"\n80점 이상 학생 수: {count}명")

def main():
    manager = GradeManager()
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
            manager.input_students()
        elif choice == "2":
            manager.print_results()
        elif choice == "3":
            manager.add_student()
        elif choice == "4":
            manager.delete_student()
        elif choice == "5":
            manager.search_student()
        elif choice == "6":
            manager.sort_students_by_total()
        elif choice == "7":
            manager.count_above_80()
        else:
            print("잘못된 입력입니다. 다시 선택하세요.")

if __name__ == "__main__":
    main()
