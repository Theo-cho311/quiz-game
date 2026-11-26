import json
from pathlib import Path


STATE_FILE = Path(__file__).resolve().parent / "state.json"


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show_question(self):
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터가 객체 형식이 아닙니다.")

        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 내용이 올바르지 않습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("선택지 내용이 올바르지 않습니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1부터 4까지의 정수여야 합니다.")

        return cls(question, choices, answer)


class QuizGame:
    def __init__(self):
        self.quizzes = self.default_quizzes()
        self.best_score = None
        self.load_state()

    def default_quizzes(self):
        return [
            Quiz(
                "달리기를 시작하기 전에 하면 좋은 것은?",
                ["준비운동", "바로 전력 질주", "움직이지 않기", "신발 벗기"],
                1,
            ),
            Quiz(
                "마라톤 풀코스의 거리는?",
                ["5km", "10km", "21.0975km", "42.195km"],
                4,
            ),
            Quiz(
                "달리기에서 페이스(pace)는 보통 무엇을 뜻할까요?",
                ["신발의 무게", "1km를 달리는 데 걸리는 시간", "하루 식사 횟수", "운동복의 크기"],
                2,
            ),
            Quiz(
                "스쿼트는 주로 어느 부위를 단련하는 운동일까요?",
                ["손가락", "목", "허벅지와 엉덩이", "손목"],
                3,
            ),
            Quiz(
                "육상 경기의 계주에서 다음 주자에게 전달하는 것은?",
                ["공", "라켓", "줄넘기", "바통"],
                4,
            ),
        ]

    def load_state(self):
        try:
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("저장 데이터가 객체 형식이 아닙니다.")

            saved_quizzes = data["quizzes"]
            saved_score = data["best_score"]

            if not isinstance(saved_quizzes, list):
                raise ValueError("퀴즈 목록이 리스트가 아닙니다.")
            if saved_score is not None and (
                type(saved_score) is not int or saved_score < 0
            ):
                raise ValueError("최고 점수가 올바르지 않습니다.")

            loaded_quizzes = [
                Quiz.from_dict(item) for item in saved_quizzes
            ]

            self.quizzes = loaded_quizzes
            self.best_score = saved_score

        except FileNotFoundError:
            # 첫 실행에는 기본 퀴즈를 사용한다.
            pass
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError,
                TypeError, ValueError) as error:
            print("저장 파일을 읽지 못해 기본 퀴즈로 시작합니다:", error)

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }

        temporary_file = STATE_FILE.with_name("state.json.tmp")

        try:
            with temporary_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")

            temporary_file.replace(STATE_FILE)
            return True

        except OSError as error:
            print("데이터 저장에 실패했습니다:", error)
            return False

    def read_number(self, prompt, minimum, maximum):
        while True:
            text = input(prompt).strip()

            if not text:
                print("번호를 입력해 주세요.")
                continue

            try:
                number = int(text)
            except ValueError:
                print("숫자로 입력해 주세요.")
                continue

            if minimum <= number <= maximum:
                return number

            print(f"{minimum}부터 {maximum}까지의 번호를 입력해 주세요.")

    def read_text(self, prompt):
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("내용을 입력해 주세요.")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0

        for quiz in self.quizzes:
            quiz.show_question()
            user_answer = self.read_number(
                "정답 번호를 입력하세요: ", 1, 4
            )

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                score += 1
            else:
                print("오답입니다.")

        print(f"결과: {len(self.quizzes)}문제 중 {score}문제 정답")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.save_state()

    def add_quiz(self):
        question = self.read_text("새 문제를 입력하세요: ")
        choices = []

        for number in range(1, 5):
            choice = self.read_text(f"선택지 {number}을 입력하세요: ")
            choices.append(choice)

        answer = self.read_number("정답 번호를 입력하세요 (1~4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        if self.save_state():
            print("퀴즈가 추가되고 저장됐습니다.")
        else:
            print("퀴즈는 현재 실행 중인 게임에만 추가됐습니다.")

    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def show_best_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 정답 수: {self.best_score}")

    def show_menu(self):
        print("\n1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")

    def run(self):
        print("운동·러닝 퀴즈 게임에 오신 것을 환영합니다!")

        try:
            while True:
                self.show_menu()
                choice = self.read_number("메뉴 번호를 입력하세요: ", 1, 5)

                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_best_score()
                else:
                    print("게임을 종료합니다.")
                    break

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 게임을 종료합니다.")
            self.save_state()


if __name__ == "__main__":
    game = QuizGame()
    game.run()