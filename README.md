# V-Coin-Trader

# installation

```bash
# Pipenvの仮想環境をプロジェクト内に作成する設定
$ echo 'export PIPENV_VENV_IN_PROJECT=1' >> ~/.zshrc

# for prod
$ cd V-Coin-Trader
$ pipenv install

# for dev
$ cd V-Coin-Trader
$ pipenv install --dev
```
- setup for run
```bash
$ python setup.py
# input your API KEYS
# generate encrypted API KEYS to ./conf/credentials.json 
```
