from logic_utils import check_guess, parse_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- parse_guess: bug fix — bounds checking ---

def test_parse_guess_valid():
    ok, value, err = parse_guess("50", 1, 100)
    assert ok is True
    assert value == 50
    assert err is None

def test_parse_guess_empty():
    ok, value, err = parse_guess("", 1, 100)
    assert ok is False
    assert value is None

def test_parse_guess_not_a_number():
    ok, value, err = parse_guess("abc", 1, 100)
    assert ok is False
    assert "not a number" in err.lower()

def test_parse_guess_below_range():
    ok, value, err = parse_guess("0", 1, 100)
    assert ok is False
    assert "between" in err

def test_parse_guess_above_range():
    ok, value, err = parse_guess("101", 1, 100)
    assert ok is False
    assert "between" in err

def test_parse_guess_at_lower_bound():
    ok, value, err = parse_guess("1", 1, 100)
    assert ok is True
    assert value == 1

def test_parse_guess_at_upper_bound():
    ok, value, err = parse_guess("100", 1, 100)
    assert ok is True
    assert value == 100

def test_parse_guess_easy_difficulty_rejects_out_of_range():
    ok, value, err = parse_guess("21", 1, 20)
    assert ok is False
    assert "between" in err

def test_parse_guess_decimal_is_accepted():
    ok, value, err = parse_guess("7.9", 1, 100)
    assert ok is True
    assert value == 7


# --- update_score: bug fix — standardized deductions and win formula ---

def test_score_win_attempt_1_gives_100():
    assert update_score(0, "Win", 1) == 100

def test_score_win_attempt_2_gives_90():
    assert update_score(0, "Win", 2) == 90

def test_score_win_attempt_3_gives_80():
    assert update_score(0, "Win", 3) == 80

def test_score_win_floors_at_10():
    assert update_score(0, "Win", 20) == 10

def test_score_too_high_deducts_5():
    assert update_score(50, "Too High", 1) == 45

def test_score_too_low_deducts_5():
    assert update_score(50, "Too Low", 1) == 45

def test_score_too_high_and_too_low_equal_deduction():
    # Bug fix: previously Too High on even attempts gave +5 instead of -5
    assert update_score(100, "Too High", 2) == update_score(100, "Too Low", 2) == 95

def test_score_unknown_outcome_unchanged():
    assert update_score(75, "Unknown", 1) == 75