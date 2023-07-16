input_str = "nitk it 2022 y 1"
values = input_str.split()
college, year, round, branch, ciwg = None, None, None, None, None
for arg in values:
    print(arg)
    if arg.isnumeric():
        if int(arg) in [2021, 2022, 2023]:
            year = arg
        elif int(arg) in [1,2,3]:
            round = arg
    elif arg.isalpha():
        if len(arg) > 3:
            college = arg
        elif len(arg) < 4 and len(arg) > 1:
            branch = arg
        elif arg in ['y', 'n']:
            ciwg = arg
print(college, year, round, branch, ciwg)