import itertools
import math
import random

s1 = {"".join(p): 1 for p in itertools.permutations("0123456789", 4)}
def get_number_of_correct_digits(secret_number, guess):
    count = 0
    for i in range(len(secret_number)):
        if secret_number[i] == guess[i]:
            count += 1
    return count

def get_number_of_misplaced_digits(secret_number, guess):
    count = 0
    for digit in guess:
        if digit in secret_number:
            count += 1
    return count - get_number_of_correct_digits(secret_number, guess)

def calculate_U(possible_feedbacks):
    U = 0
    for count in possible_feedbacks.values():
        if count > 0:
            U += count * math.log(count)
    return U

def generate_possible_solutions(previous_guess, previous_feedback, possible_solutions):
    new_possible_solutions = {}
    for solution, count in possible_solutions.items():
        guess = str(solution)
        correct_digits = get_number_of_correct_digits(previous_guess, guess)
        misplaced_digits = get_number_of_misplaced_digits(previous_guess, guess)

        if correct_digits == previous_feedback[0] and misplaced_digits == previous_feedback[1]:
            if guess not in new_possible_solutions:
                new_possible_solutions[guess] = 0
            new_possible_solutions[guess] += count

    return new_possible_solutions

# 输入ps，输出一个最佳猜测
def get_next_guess(possible_solutions):
    next_guess_U = {}
    for Y in s1:
        possible_feedbacks = {}
        for X in possible_solutions:
            key = (get_number_of_correct_digits(X, Y), get_number_of_misplaced_digits(X, Y))
            count = possible_feedbacks.get(key, 0)
            possible_feedbacks[key] = count + 1
        U = calculate_U(possible_feedbacks)
        next_guess_U[Y] = U
    print(next_guess_U)
    return min(next_guess_U, key=next_guess_U.get)
def main():
    print("请心中想一个0-9不重复的四位数，然后按回车键继续...")
    input()

    possible_solutions = {"".join(p) : 1 for p in itertools.permutations("0123456789", 4)}
    print(len(possible_solutions))
    # previous_guess = list(possible_solutions.keys())[random.randint(1, 5039)]
    previous_guess = '1234'

    while len(possible_solutions) > 1:
        print("我的猜测是：" + previous_guess)
        print("请告诉我猜对的数字个数（位置正确）：")
        correct_digits = int(input())
        print("请告诉我猜对的数字个数（位置错误）：")
        misplaced_digits = int(input())

        feedback = (correct_digits, misplaced_digits)
        possible_solutions = generate_possible_solutions(previous_guess, feedback, possible_solutions)
        next_guess = get_next_guess(possible_solutions)

        print("可能性的种数：", len(possible_solutions))
        previous_guess = next_guess

    print("你心中想的数字是：" + possible_solutions.popitem()[0])

if __name__ == "__main__":
    main()