# Tennis Thesis
Software used to create models described in my BSE thesis titled **"Predicting the results of tennis matches using machine learning"** at **Wasrsaw University of Technology** (Poland), field of study **Applied Computer Science**.

## TENNIS DATA
Historical data used in the project can be found in Jeff Sackman repository  
https://github.com/JeffSackmann  
I Wouldn't be able to create this project without it 

## How to run
**Requirements**

- Python 3.12  
- Jupyter Notebook or VSCode with Jupyter plugin  
- Git

1. Copy repository from GitHub
``` bash
git clone https://github.com/MarcinCho/TennisThesis.git
```

2. Change the working directory to project's directory

``` bash
cd TennisThesis/
```
3. Create virtual enviorment 
``` bash
python3 -m venv .venv
```
4. Activate venv
``` bash
source .venv/bin/activate
```
5. Install dependencies

    Don't forget to upgrade pip first
``` bash
python3 -m pip install --upgrade pip
```
Instal dependencies from requierments.txt

```bash
python3 -m pip install -r requirements.txt
``` 
### You can skip steps 6 and 7, The preprocessed files are availible in this repository
<font color="gray">
6. Open the ***preproces.ipynb*** notebook select WTA or ATP federation in first cell and run all the cells 

```python
preprocess.ipynb

def combine_years(where):
    path = where
    files = os.listdir(path)
    combined_years_df = pd.concat(
        [pd.read_csv(f'{path}/{file}') for file in files if file.endswith('.csv')], ignore_index=True)
    return combined_years_df
df = combine_years('db/atp') # <- change it here
df.describe()

```
7. Open the ***feature_enginering.ipynb*** notebook and run all the cells
</font>

8. Select one of the notbooks in /machine_learning_models and run all the cells  
 <font color="red">**IT MAY TAKE A LONG TIME**</font>

9. Take a look at the results in notebooks.


## Description
In this study, we explored the potential of applying machine learning algorithms to predict the winners of tennis matches. Models were developed based on various algorithms, such as decision trees, logistic regression, random forest, gradient boosting, and artificial neural networks. A key element was also the construction of a database, representing the statistics of players based on their previous matches. Various methods and technologies were used, including Python, Scikit-learn, TensorFlow, Keras, and Pandas. The modeling involved hyperparameter optimization, feature selection, and model performance evaluation. The most important features turned out to be, among others, the position in the WTA ranking, the number of points in the ranking, the total number of matches played, and the percentage of wins. Although the results did not reach the level of the best studies in this field, they were satisfactory and indicated the potential of the methods used. The logistic regression model proved to be the most precise, while the decision tree was the least precise. The AUC index indicated that the models are acceptable. The work emphasizes that predicting the outcomes of tennis matches is complicated due to many factors, including the randomness in service determination. Despite certain limitations, the models achieved satisfactory results and provide a basis for further research in this field.


## Main languages, libraries and frameworks used
* Python - https://www.python.org/
* Numpy - https://numpy.org/
* Pandas - https://pandas.pydata.org/
* Scikit-learn - https://scikit-learn.org/stable/
* TensorFlow - https://www.tensorflow.org/
* Keras - https://keras.io/

## Ref

- Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 3rd Edition  
    https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/

- Glicko System  
http://www.glicko.net/glicko.html

- Predykcja wyników meczów tenisowych z wykorzystaniem uczenia maszynowego  
https://repo.pw.edu.pl/info/bachelor/WUTd62e7702ba3a44ff94449730d3de26e5/

- Artificial Intelligence: A Modern Approach
https://aima.cs.berkeley.edu/

