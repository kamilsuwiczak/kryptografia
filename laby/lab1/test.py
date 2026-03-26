from collections import Counter
from generator import main

def single_bits_test(series):
    count_0 = series.count(0)
    count_1 = series.count(1)
    total = len(series)
    print(f"Count of 0s: {count_0}, Count of 1s: {count_1}, Total: {total}")
    if count_1>9725 and count_1<10275:
        print("Single bits test passed.")
    else:
        print("Single bits test failed.")

def poker_test(series):
    n = len(series)
    m = 4
    k = n // m 
    groups = [tuple(series[i:i+m]) for i in range(0, k*m, m)]
    count = Counter(groups)
    sum_squares = sum(v**2 for v in count.values())
    poker_statistic = (16 / k) * sum_squares - k
    print(f"Poker test statistic: {poker_statistic}")
    if poker_statistic > 2.16 and poker_statistic < 46.17:
        print("Poker test passed.")
    else:
        print("Poker test failed.")

def series_test(series):
    runs_0 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    runs_1 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    current_bit = series[0]
    current_length = 1
    for i in range(1, len(series)):
        if series[i] == current_bit:
            current_length += 1
        else:
            length_category = current_length if current_length <= 6 else 6
            
            if current_bit == 0:
                runs_0[length_category] += 1
            else:
                runs_1[length_category] += 1

            current_bit = series[i]
            current_length = 1

    length_category = current_length if current_length <= 6 else 6
    if current_bit == 0:
        runs_0[length_category] += 1
    else:
        runs_1[length_category] += 1

    intervals = {
        1: (2315, 2685),
        2: (1114, 1386),
        3: (527, 723),
        4: (240, 384),
        5: (103, 209),
        6: (103, 209)
    }

    test_passed = True

    for bit_val, runs in [("0", runs_0), ("1", runs_1)]:
        for length in range(1, 7):
            count = runs[length]
            min_val, max_val = intervals[length]
            
            if min_val > count or count > max_val:
                test_passed = False
                

    if test_passed:
        print("Series test passed")
    else:
        print("Series test failed")

    return test_passed

def long_series_test(series):
    max_run_length = 0
    current_length = 1
    current_bit = series[0]

    for i in range(1, len(series)):
        if series[i] == current_bit:
            current_length += 1
        else:
            if current_length > max_run_length:
                max_run_length = current_length
            
            current_bit = series[i]
            current_length = 1

    if current_length > max_run_length:
        max_run_length = current_length

    print(f"Longest series: {max_run_length}")
    
    test_passed = max_run_length < 26
    
    if test_passed:
        print("Long series test passed")
    else:
        print("Long series test failed")

    return test_passed

series = main()

print(f"Read series: {series}, length: {len(series)}")
single_bits_test(series)
print("========================")
poker_test(series)
print("=================================")
series_test(series)
print("=============================")
long_series_test(series)