# Vector Space Based Information Retrieval System

Use python version >= 3.6

## Execution Instructions

1. Install required dependencies

```
   $ pip install -r requirements.txt
```

2. To test a particular model, navigate to the respective folder.
   For basic-vector-space-model 
```
   $ cd model-name
   for eg: cd basic-vector-space-model 
```

3. Index creation
```
   filepath refers to the dataset file path
   $ python3 index_creation.py --filepath

   for eg: $ python3 index_creation.py ../dataset/wiki_00 
```

4. Testing queries
```
   $ python3 test_queries.py
```
``` 
    Sample Output:
    
    Input query(Ctrl-C to exit): The Indian Cricket Team
    Retrieving relevant documents...
    Document ID Document Name                                               Score
    ---------   ----------------------------------------------------------  --------
    1249        Indian cricket team in the West Indies in 2017              0.358479
    1247        Indian cricket team in Sri Lanka in 2017                    0.347235
    1246        Zimbabwean cricket team in Sri Lanka in 2017                0.274411
    1245        Pakistani cricket team in Bangladesh in 2017                0.264218
    2850        Afghan cricket team in the West Indies in 2017              0.263237
    1472        List of Bangladesh Under-23 international cricketers        0.24604
    5438        Indian Navy (football club)                                 0.244117
    1299        Bangladesh national under-23 cricket team                   0.236159
    2694        List of Bangladesh A international cricketers               0.215802
    2605        Irish cricket team against Afghanistan in India in 2016–17  0.207011
```


  

