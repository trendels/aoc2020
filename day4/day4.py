#!/usr/bin/env python3
import re


def read_batch(f):
    passport = {}
    for line in f:
        if not line.strip():
            yield passport
            passport = {}
        for token in line.split():
            k, v = token.split(":")
            passport[k] = v
    if passport:
        yield passport


def is_valid(passport):
    required = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    return all(field in passport for field in required)


def check_height(h, unit):
    if unit == "cm":
        return 150 <= int(h) <= 193
    if unit == "in":
        return 59 <= int(h) <= 76
    return False


RULES = {
    "byr": (r"\d{4}", lambda s: 1920 <= int(s) <= 2002),
    "iyr": (r"\d{4}", lambda s: 2010 <= int(s) <= 2020),
    "eyr": (r"\d{4}", lambda s: 2020 <= int(s) <= 2030),
    "hgt": (r"(\d+)(cm|in)", check_height),
    "hcl": (r"#[0-9a-f]{6}", lambda _: True),
    "ecl": (r"amb|blu|brn|gry|grn|hzl|oth", lambda _: True),
    "pid": (r"\d{9}", lambda _: True),
    "cid": None,
}


def is_valid_new(passport, rules=RULES):
    for k, v in rules.items():
        if v is None:
            continue
        if k not in passport:
            return False
        pattern, validator = v
        m = re.fullmatch(pattern, passport[k])
        if not m:
            return False
        args = m.groups() or [m.group(0)]
        if not validator(*args):
            return False
    return True


if __name__ == "__main__":
    from io import StringIO
    from textwrap import dedent

    f = StringIO(dedent(
    '''
    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in
    '''
    ).strip())
    assert len([p for p in read_batch(f) if is_valid(p)]) == 2

    print("part 1")
    with open("input.txt") as f:
        num_valid = len([p for p in read_batch(f) if is_valid(p)])
        print(num_valid)

    f = StringIO(dedent(
    '''
    eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946

    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007
    '''
    ).strip())
    assert not any(is_valid_new(p) for p in read_batch(f))

    f = StringIO(dedent(
    '''
    pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f

    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022

    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
    '''
    ).strip())
    assert all(is_valid_new(p) for p in read_batch(f))

    print("part 2")
    with open("input.txt") as f:
        num_valid = len([p for p in read_batch(f) if is_valid_new(p)])
        print(num_valid)
