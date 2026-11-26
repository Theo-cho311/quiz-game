class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show_question(self):
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(number, choice)

    def check_answer(self, user_answer):
        return user_answer == self.answer

quiz1 = Quiz(
    "달리기를 시작하기 전에 하면 좋은 것은?",
    ["준비운동", "바로 전력 질주", "움직이지 않기", "신발 벗기"],
    1
)

quiz2 = Quiz(
    "마라톤 풀코스의 거리는?",
    ["5km", "10km", "21.0975km", "42.195km"],
    4
)

quiz3 = Quiz(
    "달리기에서 페이스(pace)는 보통 무엇을 뜻할까요?",
    ["신발의 무게", "1km를 달리는 데 걸리는 시간", "하루 식사 횟수", "운동복의 크기"],
    2
)

quiz4 = Quiz(
    "스쿼트는 주로 어느 부위를 단련하는 운동일까요?",
    ["손가락", "목", "허벅지와 엉덩이", "손목"],
    3
)

quiz5 = Quiz(
    "육상 경기의 계주에서 다음 주자에게 전달하는 것은?",
    ["공", "라켓", "줄넘기", "바통"],
    4
)

quizzes = [quiz1, quiz2, quiz3, quiz4, quiz5]
best_score = None
print("등록된 퀴즈 수:", len(quizzes))

print("운동·러닝 퀴즈 게임에 오신 것을 환영합니다!")

while True:
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 최고 점수 확인")
    print("5. 종료")

    choice = input("메뉴 번호를 입력하세요: ").strip()

    if choice == "1":
        if not quizzes:
            print("등록된 퀴즈가 없습니다.")
            continue
        score = 0
        for quiz in quizzes:
            quiz.show_question()

            while True:
                try:
                    user_answer = input("정답 번호를 입력하세요: ").strip()
                    user_answer = int(user_answer)

                    if 1 <= user_answer <= 4:
                        break

                    print("1부터 4까지의 번호를 입력해 주세요.")
                except ValueError:
                    print("숫자로 입력해 주세요.")

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                score += 1
            else:
                print("오답입니다.")
        print("결과:", len(quizzes), "문제 중", score, "문제 정답")
        if best_score is None or score > best_score:
            best_score = score        
    elif choice == "2":
        while True:
            question = input("새 문제를 입력하세요: ").strip()
            if question:
                break
            print("문제 내용을 입력해 주세요.")
        choices = []
        for number in range(1, 5):
            while True:
                choice_text = input(f"선택지 {number}을 입력하세요: ").strip()
                if choice_text:
                    choices.append(choice_text)
                    break
                print("선택지 내용을 입력해 주세요.")
        while True:
            try:
                answer = int(input("정답 번호를 입력하세요 (1~4): ").strip())
                if 1 <= answer <= 4:
                    break
                print("1부터 4까지의 번호를 입력해 주세요.")
            except ValueError:
                print("숫자로 입력해 주세요.")
        new_quiz = Quiz(question, choices, answer)
        quizzes.append(new_quiz)
        print("퀴즈가 추가됐습니다.")
    elif choice == "3":
        if not quizzes:
            print("등록된 퀴즈가 없습니다.")
        else:
            for number, quiz in enumerate(quizzes, start=1):
                print(number, quiz.question)
    elif choice == "4":
        if best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print("최고 정답 수:", best_score)
    elif choice == "5":
        print("게임을 종료합니다.")
        break
    else:
        print("1부터 5까지의 번호를 입력해 주세요.")