# Koios1143 ChatBot (v2.4)
現存於line上的chat bot
參考教學網站: https://yaoandy107.github.io/line-bot-tutorial/

## Bot LineID
```
@328mmikv
```

## What's new
- 改善輸出格式
- 改善檔案位置及格式
- 傳送位置資訊即可取得半徑1km內的口罩資訊
- 將access token、secret存放於config.yml
- 新增.gitignore
- 修正maskdata_GPS錯誤內容
- 新增pos_out.json存取店家座標
- 若查詢時間與資料時間差距30min以上會更新資料

## Features
- 鸚鵡式回話

    當使用者輸入時，會回覆`[使用者傳送的文字] + てす`
- 指令操作
    - `--help` 詢問可使用指令
    - `whoami` 回覆bot名稱
    - `mask+[郵遞區號前三碼]` 回覆此區域口罩剩餘情況，一次輸出10筆資料
    - `+` 顯示更多的mask查詢結果
    - `zipcode+[城市(縣/市)][區域(鄉/鎮/市/區)]` 查詢郵遞區號
- 其他操作
    - 傳送位置資訊 回復所在區域半徑1KM內的口罩資訊

**mask data from [健康保險資料開放服務](https://data.nhi.gov.tw/Datasets/DatasetResource.aspx?rId=A21030000I-D50001-001)**

**Author:** Koios1143

**e-mail:** ken1357924681010@gmail.com

**time:** 2020/3/7

