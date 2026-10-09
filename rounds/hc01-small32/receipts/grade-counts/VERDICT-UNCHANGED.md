# Verdict code unchanged

`night_grade_counts.py` is an additive copy of the Studio original. Its unified diff (`night_grade_counts.diff`) contains zero removed source lines. The existing `rec.update(pass_=g["pass"], outcome=g["outcome"], ...)` verdict row is byte-for-byte identical to the original. The added capture hook passes the original classifier the exact same positional and keyword arguments and returns its result unchanged; count parsing runs only after that verdict update.

Evidence: source SHA-256 `4f35bbe96e506e0f651472d13c345562ade659c10faa96c25c8fb2c20f9b40e0`; instrumented SHA-256 `07570bdba47c539ac24e2002e867cd2555251bae5b693c9aeebaaa0d8be2b940`; diff SHA-256 `70fd2f3933c8d4e0de06834998b839c90e505846b26bf24b98000eb6321a3ba6`. The count parser returns only integer totals and a status string, then clears the full-output reference before writing the row.
