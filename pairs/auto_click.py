import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chromeを起動してpairsを開く
driver = webdriver.Chrome()
driver.get("https://pairs.lv/search/all")
print("pairsを開きました。ログインしてください。")
print("ログインが完了して検索ページが表示されたら、Enterキーを押してください。")
input(">>> Enterで自動処理を開始します...")

wait = WebDriverWait(driver, 20)

# /search/allでなければ再度アクセス
if "/search/all" not in driver.current_url:
    driver.get("https://pairs.lv/search/all")
    time.sleep(3)


def click_next_button():
    """JavaScriptで「次のお相手」ボタンを探してクリック"""
    js = """
    var titles = document.querySelectorAll('svg title');
    for (var i = 0; i < titles.length; i++) {
        if (titles[i].textContent === '次のお相手') {
            var btn = titles[i].closest('button');
            if (btn) {
                btn.click();
                return true;
            }
        }
    }
    return false;
    """
    return driver.execute_script(js)


def get_current_li_index():
    """現在開いているお相手のli要素のインデックスを取得"""
    js = """
    var links = document.querySelectorAll('#maincontent ul li a');
    var currentUrl = window.location.href;
    for (var i = 0; i < links.length; i++) {
        if (currentUrl.includes(links[i].getAttribute('href'))) {
            return i;
        }
    }
    return -1;
    """
    return driver.execute_script(js)


def close_modal():
    """モーダルを閉じる（「お相手詳細を閉じる」ボタンをクリック）"""
    js = """
    var titles = document.querySelectorAll('svg title');
    for (var i = 0; i < titles.length; i++) {
        if (titles[i].textContent === 'お相手詳細を閉じる') {
            var btn = titles[i].closest('button');
            if (btn) {
                btn.click();
                return true;
            }
        }
    }
    var closeBtn = document.querySelector('#dialog-root button');
    if (closeBtn) {
        closeBtn.click();
        return true;
    }
    return false;
    """
    return driver.execute_script(js)


def scroll_to_bottom():
    """ページの一番下までスクロール"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def click_li_by_index(index):
    """指定インデックスのli内のaタグをクリック"""
    js = f"""
    var links = document.querySelectorAll('#maincontent ul li a');
    if (links.length > {index} && {index} >= 0) {{
        links[{index}].click();
        return true;
    }}
    return false;
    """
    return driver.execute_script(js)


def get_total_li_count():
    """li要素の総数を取得"""
    return driver.execute_script(
        "return document.querySelectorAll('#maincontent ul li a').length;"
    )


def open_profile_and_loop(start_index):
    """プロフィールを開いて「次のお相手」を繰り返しクリック。ボタンが無くなったらインデックスを返す"""
    global click_count

    if not click_li_by_index(start_index):
        print(f"インデックス {start_index} のお相手が見つかりません。")
        return -1

    print(f"\nお相手 [{start_index}] のプロフィールを開きました")
    time.sleep(5)

    # 最初のクリックを待機して実行
    for attempt in range(20):
        if click_next_button():
            click_count += 1
            print(f"「次のお相手」ボタンをクリックしました（{click_count}回目）")
            break
        print(f"ボタンを探しています... ({attempt + 1}/20)")
        time.sleep(1)
    else:
        print("最初のボタンが見つかりませんでした。")
        return start_index

    # 2秒後に再度クリック
    time.sleep(2)
    if click_next_button():
        click_count += 1
        print(f"「次のお相手」ボタンをクリックしました（{click_count}回目）")

    # 1〜3秒のランダム間隔で繰り返しクリック
    fail_count = 0
    while True:
        random_wait = random.uniform(1, 3)
        print(f"{random_wait:.2f}秒待機中...")
        time.sleep(random_wait)

        if click_next_button():
            click_count += 1
            fail_count = 0
            print(f"「次のお相手」ボタンをクリックしました（{click_count}回目）")
        else:
            fail_count += 1
            if fail_count >= 3:
                current_index = get_current_li_index()
                print(f"\nボタンが3回連続見つかりません。現在のインデックス: {current_index}")
                return current_index if current_index >= 0 else start_index + 20
            print(f"ボタンが見つかりません。リトライ... ({fail_count}/3)")
            time.sleep(1)


# === メインループ ===
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#maincontent")))
current_index = 0
click_count = 0

try:
    while True:
        total = get_total_li_count()
        print(f"\n現在のリスト数: {total}, 開始インデックス: {current_index}")

        if current_index >= total:
            print("全てのお相手を処理しました。スクロールして新しいお相手を読み込みます...")
            scroll_to_bottom()
            wait_time = random.uniform(10, 15)
            print(f"{wait_time:.1f}秒待機中（新しいお相手の読み込み待ち）...")
            time.sleep(wait_time)
            new_total = get_total_li_count()
            if new_total <= total:
                print("新しいお相手が読み込まれませんでした。もう一度スクロールします...")
                scroll_to_bottom()
                time.sleep(10)
                new_total = get_total_li_count()
                if new_total <= total:
                    print("これ以上お相手が見つかりません。終了します。")
                    break
            continue

        # プロフィールを開いて「次のお相手」ループ
        last_index = open_profile_and_loop(current_index)

        # モーダルを閉じる
        print("モーダルを閉じます...")
        close_modal()
        time.sleep(2)

        # 一番下までスクロール
        print("ページ下部までスクロールします...")
        scroll_to_bottom()
        wait_time = random.uniform(10, 15)
        print(f"{wait_time:.1f}秒待機中（新しいお相手の読み込み待ち）...")
        time.sleep(wait_time)

        # 次のお相手のインデックスを設定
        if last_index >= 0:
            current_index = last_index + 1
        else:
            current_index += 1

        print(f"次のインデックス: {current_index}")

except KeyboardInterrupt:
    print(f"\n終了しました。合計 {click_count} 回クリックしました。")
except Exception as e:
    print(f"\nエラーが発生しました: {e}")
    print(f"合計 {click_count} 回クリックしました。")
