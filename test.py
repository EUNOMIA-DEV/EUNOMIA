import os
import sys
import time
from collections import defaultdict
from os import walk

import pytest
import sh

user_assigned_path = str(sys.argv[1])
assert user_assigned_path in {'e', 'b', 'o'}, f"you must enter the valid path"

helper_mapping = {
    "e": "emcc",
    "b": "emcc-binaryen",
    "o": "emcc-O3",
}

user_assigned_path = helper_mapping[user_assigned_path]
testcase_dir = f'./Wasm-samples/c_logic_bombs/{user_assigned_path}'
cmd_lists = []

candidates = []
for _, _, files in walk(testcase_dir):
    for file in files:
        if file.endswith('.wasm'):
            candidates.append(file[: -5])

candidates.sort()

for case in candidates:
    case += '.wasm'
    file_path = os.path.join(testcase_dir, case)
    cmd_lists.append(['eunomia_entry', '-f', file_path, '-s',
                     '--onlyfunc', 'main', '--need_mapper'])

result = defaultdict(list)
python_cmd = sh.Command('/usr/bin/python3')
for i, cmd in enumerate(cmd_lists):
    try:
        print('Case: ', candidates[i])
        for _ in range(1):
            start = time.perf_counter()
            python_cmd(cmd)
            end = time.perf_counter()
            result[candidates[i]].append("{:.3f}".format(end - start))
    except sh.ErrorReturnCode as e:
        print(e)
        pytest.fail(e)

# print result
for k, v in result.items():
    print(f"{k},{','.join(v)}")

print('''
 _____
|   __|_ _ ___ ___ ___ ___ ___
|__   | | |  _|  _| -_|_ -|_ -|
|_____|___|___|___|___|___|___|
''')
