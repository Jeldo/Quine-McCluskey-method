def DecToBin(decimal, variables):  # 십진수를 이진수 문자열로 리턴
    binary = str(bin(decimal))[2:]
    binary = "0" * (variables - len(binary)) + binary
    return binary


def GetMintermList(input):  # 파일로부터 숫자들을 입력받아서 minterm들을 리스트에 저장시키고 리스트 반환
    minlist = []
    variables = int(input[0])
    numofmint = int(input[1])
    for i in range(0, numofmint):
        minlist.append(DecToBin(int(input[i + 2]), variables))
    return minlist


def GetNums(minlist):  # 초기 minterm들을 입력받아 십진수로 이루어진 리스트로 반환
    numlist = []
    for i in range(0, len(minlist)):
        numlist.append(int(minlist[i], 2))
    return numlist


def Grouping(i_group, variables):  # 그룹화 되지 않은 minterm의 리스트, 변수의 개수를 통해 그룹화 이후 빈칸이 제거된 리스트 반환
    group = [[] for g in
             range(variables + 1)]  # group list 안에 1의 갯수에 따른 list를 만들고 1의 개수에 따라 그룹화, 변수의 개수보다 1개 많은 그룹이 필요하다.
    b_group = []
    for i in range(0, len(i_group)):  # minterm list의 개수만큼 반복한다. 그룹화 진행
        onecount = 0
        for j in range(0, variables):  # 변수의 개수만큼 반복하면서 1의 개수 얻어서 그룹화
            if i_group[i][j] == "1":
                onecount += 1
        group[onecount].append(i_group[i])
    for i in range(0, len(group)):  # 빈 리스트를 제거
        if group[i] != []:
            b_group.append(group[i])
    return b_group


def Func(group, variables, PIcount, PI):  # 그룹화 되어있는 minterm의 그룹을 체크하고 재그룹화후 반환.
    ungrouped = []
    # group=Grouping(group,variables)
    for i in range(0, len(group) - 1):  # group의 개수-1번만큼 반복 :: 마지막 그룹의 minterm들은 비교할 대상이 없으므로
        for j in range(0, len(group[i])):  # group[i]의 리스트 안의 개수만큼 반복
            for k in range(0, len(group[i + 1])):  # group[i+1]의 리스트 안의 개수만큼 반복
                new_min = ""
                differ = 0
                for bit in range(0, variables):  # 변수 개수만큼 비교
                    if group[i][j][variables - bit - 1] == group[i + 1][k][
                        variables - bit - 1]:  # 다음 그룹과의 minterm의 각 자리를 비교, 같으면 그대로 다르면 "-"로 변경후 저장
                        new_min = group[i][j][variables - bit - 1] + new_min
                    else:
                        new_min = "2" + new_min
                        differ += 1
                if new_min not in ungrouped and differ == 1:  # 중복은 패스
                    ungrouped.append(new_min)
                if differ == 1:
                    PIcount[group[i][j]] += 1
                    PIcount[group[i + 1][k]] += 1
                    PIcount[new_min] = 0
                    PI[new_min] = (PI[group[i][j]].union(PI[group[i + 1][k]]))

    group = Grouping(ungrouped, variables)
    return group, PIcount, PI


def is_empty(any):
    if any:
        return False
    else:
        return True


def convert(PI):
    newPI = []
    for i in range(0, len(PI)):
        PIstr = ""
        for j in range(0, len(PI[i][0])):
            if PI[i][0][j] == "2":
                PIstr = PIstr + "-"
            else:
                PIstr = PIstr + PI[i][0][j]
        newPI.append(PIstr)
    return newPI


def solution(input):
    PIcount = {}
    PI = {}
    EPI = []
    NEPI = []
    minterms = GetMintermList(input)
    for i in range(0, len(minterms)):
        PI[minterms[i]] = set([GetNums(minterms)[i]])
        PIcount[minterms[i]] = 0
    variables = len(minterms[0])
    group = Grouping(minterms, variables)
    i = 0
    while group != []:
        group, PIcount, PI = Func(group, variables, PIcount, PI)
        if group == []:
            break
        i += 1
    PI_list = list(PI.items())
    PIcount_list = list(PIcount.items())
    PIs = []
    PI2 = []
    for i in range(0, len(PIcount_list)):
        if PIcount_list[i][1] == 0:
            PIs.append((PI_list[i][0]))
            PI2.append(set(PI_list[i][1]))
            if len(PI2) == 1:
                EPI.append(PI_list[i])
            else:
                for j in range(0, len(PI2)):
                    checker = 0
                    target = PI2[j]
                    for k in range(0, len(PI2)):
                        if is_empty(target - PI2[k]):
                            if target == PI2[k]:
                                pass
                            else:
                                checker += 1
                        else:
                            checker += 1
                    if checker == 1:
                        if PI_list[i] not in EPI:
                            EPI.append(PI_list[i])
                    else:
                        if PI_list[i] not in NEPI:
                            NEPI.append(PI_list[i])

    newEPI = convert(EPI)
    newNEPI = convert(NEPI)
    answer = []
    answer.append("EPI")
    if newEPI:
        for i in range(0, len(newEPI)):
            answer.append(newEPI[i])
    answer.append("NEPI")
    if newNEPI:
        for i in range(0, len(newEPI)):
            answer.append(newNEPI[i])
    return answer
