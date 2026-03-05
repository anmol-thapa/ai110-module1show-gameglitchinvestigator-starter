def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    #
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIXME: Logic breaks here — no bounds check existed; any number was accepted regardless of difficulty range
    # FIX: Added low/high parameters to parse_guess and reject out-of-range values with a clear error message
    if value < low or value > high:
        return False, None, f"Please enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return outcome.

    Returns: "Win", "Too High", or "Too Low"
    """
    # FIXME: Logic breaks here — secret was cast to str on even attempts, causing TypeError on int vs str comparison
    # FIX: Removed the even/odd type-switching of secret in app.py so both values are always ints
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIXME: Logic breaks here — formula used (attempt_number + 1), giving 80 pts on attempt 1 instead of 100; also Too High on even attempts rewarded +5 instead of deducting 5
        # FIX: Changed formula to (attempt_number - 1) so attempt 1 = 100 pts; standardized all wrong guesses to -5
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score