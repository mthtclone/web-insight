# ၁။ လိုအပ်တဲ့ Library များကို Import လုပ်ခြင်း
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ၂။ Dataset ကို Load လုပ်ခြင်း (Iris Dataset ကို sklearn ကနေ တိုက်ရိုက်ယူသုံးလို့ရပါတယ်)
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names) # Features (Sepal Length, Sepal Width, Petal Length, Petal Width)
y = target = iris.target # Target (Flower Species: 0, 1, 2)

# ဒေတာ ပထမပိုင်းကို ကြည့်ရှုခြင်း
print("--- Data Sample ---")
print(X.head())

# ၃။ Data Split (Training နှင့် Testing အဖြစ် ၈၀% နှင့် ၂၀% ခွဲထုတ်ခြင်း)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ၄။ Machine Learning Model လေ့ကျင့်ခြင်း (KNN ကို အသုံးပြုထားပါသည်)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# ၅။ မော်ဒယ်ကို Evaluate လုပ်ခြင်း (Test Data ဖြင့် စမ်းသပ်ခြင်း)
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# Confusion Matrix ကြည့်ရှုခြင်း
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ၆။ New User Input ဖြင့် Prediction ပြုလုပ်ခြင်း (အသစ်ထည့်မယ့် ပန်းရဲ့ အတိုင်းအတာများ)
# ဥပမာ - [Sepal Length, Sepal Width, Petal Length, Petal Width]
new_flower = [[5.1, 3.5, 1.4, 0.2]] 
prediction = knn.predict(new_flower)
predicted_species = iris.target_names[prediction[0]]

print(f"\nPredicted Flower Species for input {new_flower}: **{predicted_species}**")