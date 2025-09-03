
import pandas as pd
import numpy as np
import re
df = pd.read_csv('E:\Python\Data science\gita_translations_all.csv')
len(df)





# Define a regex pattern to match one or more words at the beginning before the key phrases
pattern = r'^([\w\s]+?)(?:\s+said|\s+spoke|\s+told|\s+asked|\s+replied|\s+addressed):'

# Apply a function to the 'Translation' column to extract the speaker's name
def get_speaker_name(translation):
    match = re.match(pattern, translation.strip())
    if match:
        # Return the first captured group, which is the speaker's name, stripped of trailing whitespace
        return match.group(1).strip()
    return None

df['Speaker_from_Translation'] = df['Translation'].apply(get_speaker_name)

#  (forward fill)
df['Speaker_from_Translation'] = df['Speaker_from_Translation'].fillna(method='ffill')

print(df['Speaker_from_Translation'].value_counts())

#  speaker names to replace
print("\n ->Simplified Categorization:")
names_to_replace = ['The Personality of Godhead', 'The Supreme Personality of Godhead', 'Lord Śrī Kṛṣṇa']
df['Speaker_from_Translation'] = df['Speaker_from_Translation'].replace(names_to_replace, 'Sri Krsna')
print(df['Speaker_from_Translation'].value_counts())

