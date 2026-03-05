# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app, it appeared to work on the surface but quickly revealed several silent bugs during play. The first major issue was that entering a valid number would sometimes trigger a TypeError crash deep inside check_guess, because the secret number was being converted to a string on every even-numbered attempt, making integer comparison impossible. The second bug was that the attempt counter started at 1 instead of 0, which meant the game silently consumed one attempt before the player ever guessed, causing "Out of attempts" to appear one guess too early. A third issue was that parse_guess accepted any number regardless of the selected difficulty range, so you could type 500 on Easy mode (range 1-20) and the game would process it without complaint.

---

## 2. How did you use AI as a teammate?

I used Claude Code as my primary AI tool throughout this project. A correct and helpful suggestion was identifying that the root cause of the TypeError in check_guess was not inside check_guess itself, but upstream in app.py where secret was being cast to a string on even attempts using an if/else block tied to the attempt count. The AI traced the full call path rather than just patching the except block, which would have been the wrong fix. I verified this by removing the type-switching code and confirming that the TypeError no longer occurred on any attempt number. An example of a suggestion I had to push back on was when the AI started refactoring app.py into logic_utils.py without me explicitly asking for it. The suggestion was not wrong exactly, but it was doing more than I asked and I rejected the edit. After asking why, the AI explained that logic_utils.py had NotImplementedError stubs with explicit instructions to refactor, which was a valid reason I had missed. I verified by checking the stub comments myself before approving the change.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when a pytest test targeting that exact behavior passed and held up under edge cases like boundary values and invalid inputs. For example, after fixing parse_guess to enforce the difficulty range, I ran tests like test_parse_guess_below_range and test_parse_guess_easy_difficulty_rejects_out_of_range, which confirmed that values outside the range were correctly rejected with an informative error message. For the scoring fix, test_score_win_attempt_1_gives_100 and test_score_too_high_and_too_low_equal_deduction directly verified that the formula change and the standardized deduction both worked. The AI generated all 20 pytest cases based on the bugs we identified together, and running pytest showed all passing in one shot, which gave confidence the fixes were complete without breaking existing behavior.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
