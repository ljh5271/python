import random  # 랜덤한 수를 생성하기 위해

board = [" " for _ in range(9)]  # 3x3 틱택토 보드를 리스트로 초기화 (총 9칸, 빈칸 " "으로 설정)

def print_board():  
    """현재 보드 상태를 출력하는 함수"""
    for i in range(0, 9, 3):  # 3칸씩 출력하여 3x3 형태 유지
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")  # 가로줄 출력
        if i < 6:  # 마지막 줄을 제외하고 구분선 출력
            print("--+---+--")

def check_winner(player):
    """승리 조건을 확인하는 함수"""
    win_cases = [  
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 가로 줄 승리 조건
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 세로 줄 승리 조건
        (0, 4, 8), (2, 4, 6)              # 대각선 승리 조건
    ]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_cases)  
    # 주어진 플레이어가 위의 조건 중 하나를 만족하면 승리 

def is_draw():
    """무승부(보드가 꽉 찼는지) 확인하는 함수"""
    return " " not in board  # 빈칸이 없으면 무승부

def player_move():
    """플레이어가 위치를 입력하고 보드를 업데이트하는 함수"""
    while True:  # 올바른 입력이 들어올 때까지 반복
        try:
            move = int(input("원하는 위치 (1~9) 입력: ")) - 1  # 1~9 입력을 받아 0~8 인덱스로 변환
            if board[move] == " ":  # 빈칸이면
                board[move] = "X"  # "X"를 해당 위치에 배치
                break  # 입력 성공 시 반복 종료
            else:
                print("이미 선택된 자리입니다. 다시 입력하세요.")  # 이미 채워진 경우 재입력 요청
        except (ValueError, IndexError):  # 숫자가 아닌 값 입력 또는 범위 초과 입력 방지
            print("1~9 사이의 숫자를 입력하세요.")

def computer_move():
    """컴퓨터가 무작위로 빈칸을 선택하는 함수"""
    empty_positions = [i for i in range(9) if board[i] == " "]  # 빈칸 리스트 생성
    move = random.choice(empty_positions)  # 무작위로 하나 선택
    board[move] = "O"  # "O"를 해당 위치에 배치

def main():
    """게임을 실행하는 함수"""
    print("틱택토 게임을 시작합니다!")  # 시작 메시지 출력
    print_board()  # 초기 보드 출력

    while True:  # 게임 루프 (승리 또는 무승부가 발생할 때까지 반복)
        player_move()  # 플레이어 차례
        print_board()  # 보드 출력
        if check_winner("X"):  # 플레이어 승리 확인
            print("플레이어 승리!")  
            break  # 승리 시 종료
        if is_draw():  # 무승부 확인
            print("무승부!")  
            break  # 무승부 시 종료

        print("\n컴퓨터 차례...")  
        computer_move()  # 컴퓨터 차례
        print_board()  # 보드 출력
        if check_winner("O"):  # 컴퓨터 승리 확인
            print("컴퓨터 승리!")  
            break  # 승리 시 종료
        if is_draw():  # 무승부 확인
            print("무승부!")  
            break  # 무승부 시 종료

if __name__ == "__main__":  
    main()  # 스크립트가 직접 실행될 때만 main() 호출 
