from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
print df
print iris.target_names
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

df.head()