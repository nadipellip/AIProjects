# Name : Pratik Nadipelli Date: 8/28/2019 Period 2
def sleep_in(weekday, vacation):
    return not weekday or vacation


def diff21(n):
    return abs(21 - n) * 2 if n > 21 else abs(21 - n)


def parrot_trouble(talking, hour):
    return talking and (hour < 7 or hour > 20)


def makes10(a, b):
    return (a + b == 10) or a == 10 or b == 10


def near_hundred(n):
    return abs(100 - n) <= 10 or abs(200 - n) <= 10


def pos_neg(a, b, negative):
    return (negative and a < 0 and b < 0) or (not negative and a * b < 0)


def not_string(str):
    return str if str[:3] == "not" else "not " + str


def missing_char(str, n):
    return str[:n] + str[n + 1:]


def hello_name(name):
    return "Hello " + name + "!"


def make_abba(a, b):
    return a + b * 2 + a


def make_tags(tag, word):
    return "<" + tag + ">" + word + "</" + tag + ">"


def make_out_word(out, word):
    return out[:len(word) // 2] + word + out[len(word) // 2:]


def extra_end(str):
    return str[-2:] * 3


def first_two(str):
    return str if len(str) < 2 else str[:2]


def first_half(str):
    return str[:len(str) / 2]


def without_end(str):
    return str[1:-1]


def first_last6(nums):
    return nums[0] == 6 or nums[-1] == 6


def same_first_last(nums):
    return nums[0] == nums[-1] if (len(nums) >= 1) else False


def make_pi(n):
    return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5][:n]


def common_end(a, b):
    return a[0] == b[0] or a[-1] == b[-1]


def sum3(nums):
    return sum(nums)


def rotate_left3(nums):
    return nums[1:] + nums[:1]


def reverse3(nums):
    return nums[::-1]


def max_end3(nums):
    return [nums[0]] * len(nums) if nums[0] > nums[-1] else [nums[-1]] * len(nums)


def sum2(nums):
    return 0 if len(nums) == 0 else nums[0] if len(nums) == 1 else nums[0] + nums[1]


def cigar_party(cigars, is_weekend):
    return (cigars >= 40 and cigars <= 60) or (is_weekend and cigars >= 40)


def date_fashion(you, date):
    return 0 if you <= 2 or date <= 2 else 2 if you >= 8 or date >= 8 else 1


def squirrel_play(temp, is_summer):
    return (temp >= 60 and temp <= 90) or (temp >= 60 and temp <= 100 and is_summer)


def caught_speeding(speed, is_birthday):
    return 0 if speed <= 60 + 5 * (is_birthday == True) else 1 if speed <= 80 + 5 * (
            is_birthday == True) else 2 if speed >= 81 + 5 * (is_birthday == True) else 99


def sorta_sum(a, b):
    return 20 if a + b >= 10 and a + b <= 19 else a + b


def alarm_clock(day, vacation):
    return "10:00" if vacation and day >= 1 and day <= 5 else "off" if (
            vacation and (day == 0 or day == 6)) else "7:00" if (day > 0 and day < 6) else "10:00"


def love6(a, b):
    return a == 6 or b == 6 or a + b == 6 or abs(a - b) == 6


def in1to10(n, outside_mode):
    return (1 <= n <= 10 and not outside_mode) or (outside_mode and (n <= 1 or n >= 10))


def sum2(nums):
    return 0 if len(nums) == 0 else nums[0] if len(nums) == 1 else nums[0] + nums[1]
