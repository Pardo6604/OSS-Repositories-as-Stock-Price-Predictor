import sklearn as sk
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('github_org_stats.csv')
numeric_data = data.select_dtypes(include=['number'])

X_train = numeric_data.iloc[:, :-1].values
y_train = numeric_data.iloc[:, -1].values

print("Features Shape:", X_train.shape)
print("Labels Shape:", y_train.shape)

def FindBestSVC():
    parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
    
    gaussian_svc = sk.svm.SVC()
    gaussian_clf = sk.model_selection.GridSearchCV(gaussian_svc, parameters)
    
    gaussian_clf.fit(X_train, y_train)

    keys = gaussian_clf.best_params_.keys()
    
    print("\nBest Parameters:")
    
    for key in keys:
        print(f'{key}: {gaussian_clf.best_params_[key]}')

    return gaussian_clf


enhanced_gaussian_svc = sk.svm.SVC(C = 10, kernel = 'rbf')
enhanced_gaussian_svc.fit(X_train, y_train)

score = enhanced_gaussian_svc.score(X_train, y_train)
print("Training Score:", score)



