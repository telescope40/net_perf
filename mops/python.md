Python Libraries & Modules
Both collections of code but with different limits. 
Libraries are a collection of Modules & Packages 
Modules are collection of functions 

PEP - Python Enhancement Proposal 
Used to document features & standards . Similar to RFC

PIP - Python Package Installer 
Easy to Install / Uninstall packages 
Solving Dependency issues 

Helpful Resources & Libraries 
requests , socket ,netutils, ipaddress, whois


#### List Comprehension
Formula - `[expression + context]`
- `[x * 2 for x in range(3)]- [0, 2, 4]`
- The brackets are the list , the context is the elements to select the expression is the function
- `[x.lower() for x in ['I AM NOT YELLING']]['i am not yelling']`
or even easier exampple 

```
employees = {'Alice' : 100000,  
'Bob' : 99817,  
'Carol' : 122908,  
'Frank' : 88123,  
'Eve' : 93121}

list_of_ppl = [person for person in employees ]

['Alice', 'Bob', 'Carol', 'Frank', 'Eve']
```

```
employees = {'Alice' : 100000,
             'Bob' : 99817,
             'Carol' : 122908,
             'Frank' : 88123,
             'Eve' : 93121}
top_earners = [(k,v) for k,v in employees.items() if v>=10000]
top_earners
[('Alice', 100000), ('Bob', 99817), ('Carol', 122908), ('Frank', 88123), ('Eve', 93121)]
```
- The expression `[(k,v) for k,v in employees.items() if v>=10000]`
	- `(k,v)` creates a tuple for context variables k & v 
**Example**
Find words with High Value information , some words provide higher value then others , some just join a sentance. Simple code to find words of 3 letters or more. 
```text = '''  
Call me Ishmael. Some years ago - never mind how long precisely - having  
little or no money in my purse, and nothing particular to interest me  
on shore, I thought I would sail about a little and see the watery part  
of the world. It is a way I have of driving off the spleen, and regulating  
the circulation. - Moby Dick'''
```
`w = [[x for x in line.split() if len(x)>3] for line in text.split('\n')]
There is two list comprehensions here 
- 1. `for line in text.split('\n')` This is the "Outer comprehension"
- 2. `[[x for x in line.split() if len(x)>3]` "This is the inner comprehension"

#### Lambda & Map Functions 
- Lambda functions define a single line function and discarded after 
	- lambda is commonly used with `map`
```
## Data  
txt = ['lambda functions are anonymous functions.',  
       'anonymous functions dont have a name.',  
       'functions are objects in Python.']  
  
  
## One-Liner  
mark = map(lambda s: (True, s) if 'anonymous' in s else (False, s), txt)  
  
  
## Result  
print(list(mark))
```

The code 
	- `mark = map(lambda s: (True, s) if 'anonymous' in s else (False, s), txt) `
		- The lambda defines a function to look for the word "anonymous" in text else it returns a boolean 

**Combining List Comprehension & Slicing**

Training for stock prices

```
price = [[9.9, 9.8, 9.8, 9.4, 9.5, 9.7],  
         [9.5, 9.4, 9.4, 9.3, 9.2, 9.1],  
         [8.4, 7.9, 7.9, 8.1, 8.0, 8.0],  
         [7.1, 5.9, 4.8, 4.8, 4.7, 3.9]]  
  
  
## One-Liner  
sample = [line[::2] for line in price]
```
This uses the slicing index of every other number for each list inside of list of price

#### Slicing to extract matching substring envs
- Slicing is the process of carving out a subsequence from an original full sequence. 
- Slicing is the basis of NumPy , Panda , TensorFlow and scikitlearn
	- `x[start:stop:step]`
		- Start is included , stop is excluded 
		- step is optional 
		- Slicing with `string.find(value)`
```
In the following example you want to find the query in the text and return its immeiate environment up to 18 positions around the found query. This is like when google provides text snippets around results for key word search. 

## Data  
letters_amazon = '''  
We spent several years building our own database engine,  
Amazon Aurora, a fully-managed MySQL and PostgreSQL-compatible  
service with the same or better durability and availability as  
the commercial engines, but at one-tenth of the cost. We were  
not surprised when this worked.  
'''  
  
## One-Liner  
find = lambda x, q: x[x.find(q)-18:x.find(q)+18] if q in x else -1  
  
  
## Result  
print(find(letters_amazon, 'SQL'))

The lambda gives two args string and query , x is the string and q is the query. 
If the query word does not appear in the string it returns 
A better way for write it might be 

find = lambda x, q: x[x.find(q)-18:x.find(q)+18] if q in x else "no results" 


```



**Example use case**
- Replace every other string with the string immediately leading it 



```
visitors = ['Firefox', 'corrupted', 'Chrome', 'corrupted',  
            'Safari', 'corrupted', 'Safari', 'corrupted',  
            'Chrome', 'corrupted', 'Firefox', 'corrupted']  
  
  
## One-Liner  
visitors[1::2] = visitors[::2]  

This indicates to start at item 1 (second vars), the skip over every other one , the reassign them to the positional args of every other item in the list 

visitors[1::2] = ['corrupted', 'corrupted', 'corrupted', 'corrupted', 'corrupted', 'corrupted']
visitors[::2] = ['Firefox', 'Chrome', 'Safari', 'Safari', 'Chrome', 'Firefox']

## Result  
print(visitors)
```

**Tracking Cardiac Cycles**
- Need to remove redundant vars 
- Clean the original list 
- Combine slicing and list concatenation 
- `matplotlib.pyplot`
	- `plot(data)` data needs to be an iterable object 
- Remove the first and last two values from the list 
- Create new list with the expected future heart rates by copying the cardiac cycles to the future time instance 
```
## Dependencies  
import matplotlib.pyplot as plt  
  
  
## Data  
cardiac_cycle = [62, 60, 62, 64, 68, 77, 80, 76, 71, 66, 61, 60, 62]  
  
  
## One-Liner  
expected_cycles = cardiac_cycle[1:-2] * 10  
This starts at the second entry of the list (60) and steps backward -2
It skips the 62 at position 0 , skips the 60 at second to last position
  
  
## Result  
plt.plot(expected_cycles)  
plt.show()
```

![[Pasted image 20230609091444.png]]

**Example find companies that pay below min wage**
- `any()` function 
- Takes an iterable such as a list and returns True is at least one evals to true 
- **Generator Expressions**
	- work like list comprehensions but without the actual list in memory
```
Our data is a dictionary of dictionaries storing the hourly wages of company employees. You want to extract a list of the companies paying below your state’s minimum wage (< $9) for at least one employee; see [Listing 2-9](https://learning.oreilly.com/library/view/python-one-liners/9781098122676/xhtml/ch02.xhtml#list2-9).

## Data  
companies = {  
    'CoolCompany' : {'Alice' : 33, 'Bob' : 28, 'Frank' : 29},  
    'CheapCompany' : {'Ann' : 4, 'Lee' : 9, 'Chrisi' : 7},  
    'SosoCompany' : {'Esther' : 38, 'Cole' : 8, 'Paris' : 18}}  
  
  
## One-Liner  
illegal = [x for x in companies if any(y<9 for y in companies[x].values())]  
  
  
## Result  
print(illegal)
```


### Formatting DBs with zip()
- `Zip` takes iterables and aggregates them into a single iterable by aligning gthe corresponding i-th values in a single tuple
- `unzip` 
```
column_names = ['name', 'salary', 'job']  
db_rows = [('Alice', 180000, 'data scientist'),  
           ('Bob', 99000, 'mid-level manager'),  
           ('Frank', 87000, 'CEO')]

db = [dict(zip(column_names, row)) for row in db_rows]


[{'name': 'Alice', 'salary': 180000, 'job': 'data scientist'}, {'name': 'Bob', 'salary': 99000, 'job': 'mid-level manager'}, {'name': 'Frank', 'salary': 87000, 'job': 'CEO'}]

```

