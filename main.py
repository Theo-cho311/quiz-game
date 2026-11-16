print("운동·러닝 퀴즈 게임에 오신 것을 환영합니다!")

while True:
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 최고 점수 확인")
    print("5. 종료")

    choice = input("메뉴 번호를 입력하세요: ").strip()

    if choice == "1":
        print("퀴즈 풀기를 선택했습니다.")
    elif choice == "2":
        print("퀴즈 추가를 선택했습니다.")
    elif choice == "3":
        print("퀴즈 목록을 선택했습니다.")
    elif choice == "4":
        print("최고 점수 확인을 선택했습니다.")
    elif choice == "5":
        print("게임을 종료합니다.")
        break
    else:
        print("1부터 5까지의 번호를 입력해 주세요.")