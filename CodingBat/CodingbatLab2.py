# Name: Pratik Nadipelli Period 2
def string_times(str, n):
    return str * n


def front_times(str, n):
    return str[:3] * n


def string_bits(str):
    return str[::2]


def string_splosion(str):
    return ("").join([str[:i] for i in range(len(str) + 1)])


def last2(str):
    return [str[i:i + 2] for i in range(len(str) - 2)].count(str[-2:])


def array_count9(nums):
    return nums.count(9)


def array_front9(nums):
    return nums[:4].count(9) > 0


def array123(nums):
    return sum([nums[i] == 1 and nums[i + 1] == 2 and nums[i + 2] == 3 for i in range(len(nums) - 2)]) > 0


def string_match(a, b):
    return sum([a[i:i + 2] == b[i:i + 2] for i in range(min(len(a), len(b)) - 1)])


def make_bricks(small, big, goal):
    return (small >= goal % 5 and goal <= big * 5) or (small >= goal - (5 * big) and goal >= big * 5)


def lone_sum(a, b, c):
    return sum([[a, b, c][i] for i in range(3) if [a, b, c].count([a, b, c][i]) <= 1])


def lucky_sum(a, b, c):
    return sum([[a, b, c][i] for i in range(3) if [a, b, c][:i + 1].count(13) == 0])


def no_teen_sum(a, b, c):
    return sum([[a, b, c][i] for i in range(3) if not (12 < [a, b, c][i] < 15 or 16 < [a, b, c][i] < 20)])


def round_sum(a, b, c):
    return int(round(a, -1) + round(b, -1) + round(c, -1))


def close_far(a, b, c):
    return abs(b - a) >= 2 and abs(c - a) >= 2 or abs(b - a) >= 2 and abs(c - b) >= 2 or abs(c - a) >= 2 and abs(
        c - b) >= 2


def make_chocolate(small, big, goal):
    return goal % 5 * (big * 5 >= goal and small >= goal % 5) + (goal - big * 5) * (
            goal >= big * 5 and small >= goal - big * 5) + -1 * (goal > big * 5 + small or goal % 5 > small)


def double_char(str):
    return "".join([str[i] * 2 for i in range(len(str))])


def count_hi(str):
    return str.count("hi")


def cat_dog(str):
    return str.count("cat") == str.count("dog")


def count_code(str):
    return sum([str[i:i + 2] == "co" and str[i + 3:i + 4] == "e" for i in range(len(str))])


def end_other(a, b):
    return (a.lower()).endswith(b.lower()) or (b.lower()).endswith(a.lower())


def xyz_there(str):
    return str.count("xyz") > str.count(".xyz")


def count_evens(nums):
    return sum(nums[i] % 2 == 0 for i in range(len(nums)))


def big_diff(nums):
    return max(nums) - min(nums)


def centered_average(nums):
    return sum(sorted(nums)[1:-1]) / (len(nums) - 2)


def sum13(nums):
    return sum([item for index, item in enumerate(nums) if not (item == 13 or (index >= 1 and nums[index - 1] == 13))])


def sum67(nums):
    sum = 0
    boo = True
    for i in range(len(nums)):
        if (nums[i] == 6):
            boo = False
        if (boo == True):
            sum += nums[i]
        if (nums[i] == 7):
            boo = True
    return sum


def has22(nums):
    return sum([nums[i] == 2 and nums[i + 1] == 2 for i in range(len(nums) - 1)]) == 1
print(str(round_sum(5,6,5)))