# Information_searcher

## Requirements
Python >= 3.5

git (for for "git clone")

pip ( for "pip install")

## Installing

```shell
git clone https://github.com/MakuhIlyukh/amb_search

pip install -r requirements.txt

```

Download file (dataset) https://drive.google.com/file/d/1gJU-kUmfGJNiiGUzU72lv0lEWxk8r71G/view?usp=sharing and paste it into a folder 'Data'

```shell

cd Information_searcher
```

## Using

You can use operations AND, OR, NOT and brackets ( ) to to compose a search expression

EXAMPLES:

```shell
python3 main.py "washington AND congression"

python3 main.py "washington AND (NOT congression)"
```

