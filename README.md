# Koios1143 ChatBot (v2.1)
現存於line上的chat bot
參考教學網站: https://yaoandy107.github.io/line-bot-tutorial/

## Bot LineID
```
@328mmikv
```

## What's new
- 口罩查詢系統Bug修正
- 為避免口罩查詢格式不清楚，無論輸入 mask+ 或 mask[ 裡面加上郵遞區號都可以成功查詢
- LINE加入好友時會傳送使用教學訊息
- 修正前一版輸出格式
- `--help` 輸出內容修正，避免使用難以理解的字詞
- 口罩查詢改為一次顯示10筆
- 口罩查詢時若查詢格式錯誤(若有使用mask前綴)會提示輸入錯誤
- `--help` 加上`mask`查詢格式說明

## Features
- 鸚鵡式回話

    當使用者輸入時，會回覆`[使用者傳送的文字] + てす`
- 指令操作
    - `--help` 詢問可使用指令
    - `whoami` 回覆bot名稱
    - `mask+[郵遞區號前三碼]` 回覆此區域口罩剩餘情況，一次輸出10筆資料
    - `+` 顯示更多的mask查詢結果

**mask data from [健康保險資料開放服務](https://data.nhi.gov.tw/Datasets/DatasetResource.aspx?rId=A21030000I-D50001-001)**

**Author:** Koios1143

**e-mail:** ken1357924681010@gmail.com

**time:** 2020/2/28

