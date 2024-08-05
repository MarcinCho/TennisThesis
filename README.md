# Tennis Thesis
Software used to create models described in my BSE thesis titled **"Predicting the results of tennis matches using machine learning"** at **Wasrsaw University of Technology** (Poland), field of study **Applied Computer Science**.

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
6. Open the Preproces notebook select WTA or ATP federation in first cell and run all the cells
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
#### Please note I'm working at 2 files  structure at the moment

7. Open the ML notebook and run all the cels <font color="red">**IT MAY TAKE A LONG TIME**</font>
```
ml.ipynb
```

8. Take a look at the results


## Description


## Technologies used

## References

https://stackoverflow.com/questions/26587527/cite-a-paper-using-github-markdown-syntax