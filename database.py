##############################
# 프로그램명: 성적관리 프로그램 (MongoDB 연동 버전)
# 작성자: 컴퓨터공학과 / 홍길동
# 작성일: 2025-04-11
# 프로그램 설명:
#   - 5명의 학생 성적(영어, C-언어, 파이썬)을 입력받고
#     총점, 평균, 학점, 등수를 계산/출력/관리하는 프로그램
#   - 삽입, 삭제, 검색, 정렬, 통계 기능 포함
#   - MongoDB 데이터베이스 연동
##############################

from pymongo import MongoClient
from datetime import datetime
import logging

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
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

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

    def to_dict(self):
        """학생 객체를 MongoDB에 저장할 딕셔너리 형태로 변환"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "english": self.english,
            "c_language": self.c_language,
            "python": self.python,
            "total": self.total,
            "average": self.average,
            "grade": self.grade,
            "rank": self.rank,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        """MongoDB에서 조회한 딕셔너리를 학생 객체로 변환"""
        student = cls(
            data["student_id"],
            data["name"],
            data["english"],
            data["c_language"],
            data["python"]
        )
        student.rank = data.get("rank", 0)
        student.created_at = data.get("created_at", datetime.now())
        student.updated_at = data.get("updated_at", datetime.now())
        return student

    def display(self):
        return (f"{self.student_id:<15}{self.name:<10}{self.english:<8}"
                f"{self.c_language:<8}{self.python:<8}{self.total:<8}"
                f"{self.average:<8.2f}{self.grade:<6}{self.rank:<6}")

class MongoGradeManager:
    def __init__(self, connection_string="mongodb://localhost:27017/", db_name="grade_management"):
        """
        MongoDB 연결 초기화
        connection_string: MongoDB 연결 문자열
        db_name: 사용할 데이터베이스 이름
        """
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client[db_name]
            self.collection = self.db.students
            
            # 학번에 인덱스 생성 (중복 방지 및 검색 성능 향상)
            self.collection.create_index("student_id", unique=True)
            
            print(f"MongoDB 연결 성공: {db_name}")
            
        except Exception as e:
            print(f"MongoDB 연결 실패: {e}")
            logging.error(f"MongoDB connection failed: {e}")
            raise

    def add_student(self):
        """새 학생 추가"""
        try:
            student_id = input("학번: ")
            
            # 중복 학번 확인
            if self.collection.find_one({"student_id": student_id}):
                print("이미 존재하는 학번입니다.")
                return
            
            name = input("이름: ")
            english = int(input("영어 점수: "))
            c_language = int(input("C-언어 점수: "))
            python = int(input("파이썬 점수: "))
            
            student = Student(student_id, name, english, c_language, python)
            
            # MongoDB에 저장
            result = self.collection.insert_one(student.to_dict())
            
            if result.inserted_id:
                print(f"학생 {name}({student_id})이 성공적으로 추가되었습니다.")
                self.calculate_ranks()
            else:
                print("학생 추가에 실패했습니다.")
                
        except ValueError:
            print("점수는 숫자로 입력해주세요.")
        except Exception as e:
            print(f"학생 추가 중 오류 발생: {e}")

    def input_students(self, count=5):
        """여러 학생 입력"""
        print(f"{count}명의 학생 정보를 입력하세요.")
        for i in range(count):
            print(f"\n{i+1}번째 학생:")
            self.add_student()

    def calculate_ranks(self):
        """등수 계산 및 업데이트"""
        try:
            # 총점 기준으로 정렬하여 조회
            students_data = list(self.collection.find().sort("total", -1))
            
            rank = 1
            prev_total = None
            
            for i, student_data in enumerate(students_data):
                if prev_total is not None and student_data["total"] == prev_total:
                    current_rank = rank
                else:
                    rank = i + 1
                    current_rank = rank
                
                # 등수 업데이트
                self.collection.update_one(
                    {"_id": student_data["_id"]},
                    {"$set": {"rank": current_rank, "updated_at": datetime.now()}}
                )
                
                prev_total = student_data["total"]
                
        except Exception as e:
            print(f"등수 계산 중 오류 발생: {e}")

    def print_results(self):
        """모든 학생 정보 출력"""
        try:
            students_data = list(self.collection.find().sort("rank", 1))
            
            if not students_data:
                print("\n학생 정보가 없습니다.")
                return

            print("\n" + " 성적관리 프로그램 ".center(80, "="))
            print("=" * 100)
            print(f"{'학번':<15}{'이름':<10}{'영어':<8}{'C-언어':<8}{'파이썬':<8}{'총점':<8}{'평균':<8}{'학점':<6}{'등수':<6}")
            print("=" * 100)

            for student_data in students_data:
                student = Student.from_dict(student_data)
                print(student.display())
                
            print("=" * 100)
            print(f"총 학생 수: {len(students_data)}명")
            
        except Exception as e:
            print(f"학생 정보 출력 중 오류 발생: {e}")

    def delete_student(self):
        """학생 삭제"""
        try:
            student_id = input("삭제할 학생의 학번 입력: ")
            
            # 삭제할 학생 정보 먼저 조회
            student_data = self.collection.find_one({"student_id": student_id})
            
            if student_data:
                result = self.collection.delete_one({"student_id": student_id})
                if result.deleted_count > 0:
                    print(f"\n학번 {student_id} 학생({student_data['name']})이 삭제되었습니다.")
                    self.calculate_ranks()  # 등수 재계산
                else:
                    print("삭제에 실패했습니다.")
            else:
                print("해당 학번의 학생을 찾을 수 없습니다.")
                
        except Exception as e:
            print(f"학생 삭제 중 오류 발생: {e}")

    def search_student(self):
        """학생 검색 (학번 또는 이름으로)"""
        try:
            key = input("검색할 학번 또는 이름 입력: ")
            
            # 학번 또는 이름으로 검색
            query = {"$or": [{"student_id": key}, {"name": key}]}
            students_data = list(self.collection.find(query))
            
            if students_data:
                print(f"\n검색 결과: {len(students_data)}명")
                print("=" * 80)
                for student_data in students_data:
                    student = Student.from_dict(student_data)
                    print(f"학번: {student.student_id}, 이름: {student.name}, "
                          f"총점: {student.total}, 평균: {student.average:.2f}, "
                          f"학점: {student.grade}, 등수: {student.rank}")
                print("=" * 80)
            else:
                print("해당 조건의 학생을 찾을 수 없습니다.")
                
        except Exception as e:
            print(f"학생 검색 중 오류 발생: {e}")

    def sort_students_by_total(self):
        """총점 기준 정렬 후 출력"""
        try:
            students_data = list(self.collection.find().sort("total", -1))
            
            if not students_data:
                print("\n학생 정보가 없습니다.")
                return
                
            print("\n총점 기준 정렬 결과:")
            print("=" * 100)
            print(f"{'학번':<15}{'이름':<10}{'영어':<8}{'C-언어':<8}{'파이썬':<8}{'총점':<8}{'평균':<8}{'학점':<6}{'등수':<6}")
            print("=" * 100)

            for student_data in students_data:
                student = Student.from_dict(student_data)
                print(student.display())
                
        except Exception as e:
            print(f"정렬 중 오류 발생: {e}")

    def count_above_80(self):
        """80점 이상 학생 수 조회"""
        try:
            count = self.collection.count_documents({"average": {"$gte": 80}})
            print(f"\n80점 이상 학생 수: {count}명")
            
            # 80점 이상 학생들의 상세 정보도 출력
            if count > 0:
                students_data = list(self.collection.find({"average": {"$gte": 80}}).sort("average", -1))
                print("\n80점 이상 학생 명단:")
                print("-" * 60)
                for student_data in students_data:
                    print(f"{student_data['name']}({student_data['student_id']}): {student_data['average']:.2f}점")
                    
        except Exception as e:
            print(f"통계 조회 중 오류 발생: {e}")

    def get_statistics(self):
        """전체 통계 정보"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_students": {"$sum": 1},
                        "avg_english": {"$avg": "$english"},
                        "avg_c_language": {"$avg": "$c_language"},
                        "avg_python": {"$avg": "$python"},
                        "avg_total": {"$avg": "$total"},
                        "max_total": {"$max": "$total"},
                        "min_total": {"$min": "$total"}
                    }
                }
            ]
            
            result = list(self.collection.aggregate(pipeline))
            
            if result:
                stats = result[0]
                print("\n=== 전체 통계 ===")
                print(f"총 학생 수: {stats['total_students']}명")
                print(f"영어 과목 평균: {stats['avg_english']:.2f}점")
                print(f"C-언어 과목 평균: {stats['avg_c_language']:.2f}점")
                print(f"파이썬 과목 평균: {stats['avg_python']:.2f}점")
                print(f"전체 평균: {stats['avg_total']:.2f}점")
                print(f"최고 총점: {stats['max_total']}점")
                print(f"최저 총점: {stats['min_total']}점")
            else:
                print("\n통계 정보가 없습니다.")
                
        except Exception as e:
            print(f"통계 조회 중 오류 발생: {e}")

    def close_connection(self):
        """MongoDB 연결 종료"""
        if self.client:
            self.client.close()
            print("MongoDB 연결이 종료되었습니다.")

def main():
    try:
        # MongoDB 연결 (필요시 연결 문자열 수정)
        manager = MongoGradeManager(
            connection_string="mongodb://localhost:27017/",
            db_name="grade_management"
        )
        
        while True:
            print("\n" + "="*50)
            print("           성적관리 프로그램 (MongoDB)")
            print("="*50)
            print("1. 학생 입력 (5명)")
            print("2. 학생 출력")
            print("3. 학생 추가")
            print("4. 학생 삭제")
            print("5. 학생 검색")
            print("6. 총점 기준 정렬")
            print("7. 80점 이상 학생 수 출력")
            print("8. 전체 통계")
            print("0. 종료")
            print("="*50)
            
            choice = input("선택: ").strip()

            if choice == "0":
                print("프로그램을 종료합니다.")
                manager.close_connection()
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
            elif choice == "8":
                manager.get_statistics()
            else:
                print("잘못된 입력입니다. 0~8 중에서 선택하세요.")
                
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
        logging.error(f"Program execution failed: {e}")

if __name__ == "__main__":
    main()