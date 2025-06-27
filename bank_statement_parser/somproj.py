import pandas as pd
import re
from collections import Counter


# Full input text (re-inserted as one large string for accurate processing)
raw_challenges = """
 Which of the following should churches prioritize more in supporting parents?  
Parenting seminars
Youth mentorship programs
Parenting seminars, Youth mentorship programs
Youth mentorship programs, Counseling and prayer support
Parenting seminars
Parenting seminars
Counseling and prayer support
Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Youth mentorship programs, Biblical literacy
Counseling and prayer support
Youth mentorship programs
Biblical literacy
Parenting seminars
They're all equally important
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Counseling and prayer support
Youth mentorship programs
Biblical literacy
Parenting seminars
Parenting seminars, Biblical literacy
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Biblical literacy
Youth mentorship programs, Biblical literacy
Parenting seminars
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy
Youth mentorship programs
Parenting seminars
Counseling and prayer support
Youth mentorship programs
Parenting seminars
Parenting seminars
Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs
Youth mentorship programs
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Parenting seminars
Biblical literacy
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Counseling and prayer support
Youth mentorship programs
Biblical literacy
Youth mentorship programs
Parenting seminars, Youth mentorship programs
Parenting seminars
Youth mentorship programs
Parenting seminars
Parenting seminars
All
Youth mentorship programs
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs
Youth mentorship programs
Biblical literacy
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Biblical literacy
Parenting seminars, Youth mentorship programs
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs
Counseling and prayer support
Biblical literacy
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Counseling and prayer support
Parenting seminars
Youth mentorship programs
Parenting seminars, Youth mentorship programs
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Counseling and prayer support
Youth mentorship programs
Parenting seminars
Youth mentorship programs, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy
Parenting seminars, Counseling and prayer support
Parenting seminars
Parenting seminars
Counseling and prayer support
Youth mentorship programs
Parenting seminars
Parenting seminars, Biblical literacy
Youth mentorship programs
Parenting seminars, Youth mentorship programs, Counseling and prayer support
Counseling and prayer support
Youth mentorship programs
Youth mentorship programs
Parenting seminars
Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Counseling and prayer support
Youth mentorship programs
Parenting seminars
Youth mentorship programs
Parenting seminars
Parenting seminars, Counseling and prayer support
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Counseling and prayer support
Counseling and prayer support
Counseling and prayer support
Youth mentorship programs
Biblical literacy
Counseling and prayer support
Youth mentorship programs
Youth mentorship programs
Parenting seminars
Youth mentorship programs
Parenting seminars, Youth mentorship programs, Biblical literacy
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support, Family Life Education and Carryout disciplinary measures when necessary.
Parenting seminars, Counseling and prayer support
Parenting seminars
Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy
Biblical literacy
Parenting seminars
Parenting seminars
Youth mentorship programs
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Youth mentorship programs
Parenting seminars
Parenting seminars, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Biblical literacy
Parenting seminars
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Counseling and prayer support
Youth mentorship programs
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support, Support groups for parents
Parenting seminars
Youth mentorship programs
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support, The church should focus on the gospel of Jesus christ, salvation, eternity, fear of God rather than prosperity and motivational messages.
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy
Parenting seminars
Parenting seminars, Biblical literacy
Counseling and prayer support
Parenting seminars
Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy
Counseling and prayer support
Parenting seminars, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs
Parenting seminars, Biblical literacy
Parenting seminars
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy
Parenting seminars, Biblical literacy
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars, Counseling and prayer support
Biblical literacy
Parenting seminars, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Teaching on discipline and consistency 
Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Parenting seminars
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support
Parenting seminars
Parenting seminars
Counseling and prayer support
Youth mentorship programs
Parenting seminars, Counseling and prayer support
Parenting seminars, Youth mentorship programs, Biblical literacy, Counseling and prayer support

"""  # Use actual full text (truncated here for demonstration)

# Split and normalize the challenges
challenges = re.split(r'[\n,]+', raw_challenges.lower())
challenges = [c.strip() for c in challenges if c.strip()]

# Count occurrences
challenge_counts = Counter(challenges)

# Convert to DataFrame
challenge_df = pd.DataFrame(challenge_counts.items(), columns=["Challenge", "Frequency"])
challenge_df = challenge_df.sort_values(by="Frequency", ascending=False).reset_index(drop=True)

# print(challenge_df)

# Save to Excel
excel_path = "Parenting_Solutions_Exact_Counts.xlsx"
challenge_df.to_excel(excel_path, index=False)

# excel_path