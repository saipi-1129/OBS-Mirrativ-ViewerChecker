# OBS-Mirrativ-ViewerChecker
mirrativの現在の視聴者一覧を配信上に表示するためのOBSスクリプト

#初期設定
1. リポジトリをクローンします:
    ```bash
    git clone https://github.com/yourusername/mirrativ-chat-viewer.git
    ```

2. 必要なライブラリをインストールします:
    ```bash
    pip install requests
    ```


#OBSの設定

Pythonのインストール場所を
ツール>スクリプト>+ボタン>ダウンロードしたapp.pyを選択>ライブIDを入力>Pythonの設定>インストールパスを指定>ソースに[MirrativUserList]を追加>


#ライブIDについて

配信URLのlive/以降を入力
例:`https://www.mirrativ.com/live/example` の場合、exampleを入力
