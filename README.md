# Data Cleansing Project

This repository contains the implementation of Data Cleansing API. And also contains the implementation of report analysis abusive word for hate speech tweet.

## Dependency

This repository requires this following softwares and dependencies to work:

- Python3
- Matplotlib
- Pandas
- Regex Python
- Seaborn
- Sqlite3
- Flask
- Flassger
- Makefile (not required)

To make work well, install all dependencies first.

## How to RUN
### API Cleansing Project

To run API 

```sh
python app.py
```

or using `make`

```sh
make run
```

After run, go to `/docs` for see swagger documentation.

### Report Analysis

data preparation:

```sh
make prepare
```

data visualization:

```sh
make report
```

All generate output will save into output directory. The powerpoint file is on `report analysis.pptx`

