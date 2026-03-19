# Pairs

## 自動クリックツール

### セットアップ手順（Mac）

ターミナルを開いて、以下のコマンドを**上から順番に1行ずつ**コピペして実行してください。

#### 1. Homebrewをインストール（まだ入っていない場合）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

途中でパスワードを聞かれたら、Macのログインパスワードを入力してください（入力中は画面に表示されません）。

#### 2. Python3をインストール

```bash
brew install python3
```

#### 3. Google Chromeがインストールされていることを確認

https://www.google.com/chrome/ からインストールしてください。

#### 4. このリポジトリをダウンロード

```bash
cd ~/Desktop
git clone https://github.com/nkkn-prog/matching-tools.git
cd matching-tools
```

#### 5. 仮想環境を作成してセットアップ

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 実行方法（Mac）

**毎回以下の3行を実行してください：**

```bash
cd ~/Desktop/matching-tools
source venv/bin/activate
python3 pairs/auto_click.py
```

---

### セットアップ手順(Windows)

#### 1. Python3をインストール

https://www.python.org/downloads/ にアクセスして「Download Python」ボタンをクリックしてインストールしてください。

**重要：** インストール画面の最初で **「Add Python to PATH」にチェックを入れて** からインストールしてください。

#### 2. Google Chromeがインストールされていることを確認

https://www.google.com/chrome/ からインストールしてください。

#### 3. このリポジトリをダウンロード

PowerShell（またはコマンドプロンプト）を開いて以下を実行してください：

```powershell
cd %USERPROFILE%\Desktop
git clone <リポジトリURL>
cd matching-tools
```

> **gitが入っていない場合：** リポジトリページから「Code」→「Download ZIP」でダウンロードし、デスクトップに解凍してください。

#### 4. 仮想環境を作成してセットアップ

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 実行方法（Windows）

**毎回以下の3行を実行してください：**

```powershell
cd %USERPROFILE%\Desktop\matching-tools
venv\Scripts\activate
python pairs/auto_click.py
```

---

### 使い方（共通）

1. auto_click.pyを実行するとChromeが自動で開きます
2. Pairsにログインしてください
3. 検索ページ（`/search/all`）が表示されたら、ターミナルに戻って **Enterキー** を押してください
4. 自動で「次のお相手」ボタンを繰り返しクリックします
5. お相手がいなくなったら、自動でスクロールして新しいお相手を読み込みます

### 停止方法

`Ctrl + C` を押してください。
