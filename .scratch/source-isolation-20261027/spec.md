# 雙來源選用驗證與 GitHub 更新

Status: complete（GitHub 0.1.2 與帳號 0.1.4 已套用，正式 discovery 零名稱碰撞）
日期：2026-10-27。使用者要求真正確認誤用情況，並更新 GitHub 版插件。

## Confirmed scope

- 使用者確認一併消除名稱碰撞：GitHub 版保留現有 package／skill 識別名，帳號版三個 skill 的名稱及目錄加上 `-alpha`。保留同一私人 plugin 身分與技能正文；替換舊路徑，不留下無後綴的舊入口。
- GitHub 來源交付版本為目前 repo 的 `0.1.2`，含翻譯、句型及回譯三個入口。提交並更新 GitHub 來源，將使用者目前固定的 GitHub 安裝切至已驗證的新 commit。
- 帳號版名稱修正目標為 `0.1.4`／English Learning Tool-alpha，使用獨立的 account-source 副本與嚴格讀回比對。
- Review 基準由使用者確認為 `1d9251610de9aac9f38ff0788b6de18a277f10b3`，涵蓋其後未提交的回譯遷移、維護工具與本輪修正。

## Verification boundary

沿用已確認的「客戶端載入 → 選取 skill → 使用者可見輸出」邊界。封裝副本與實際 ZIP、帳號完整讀回、固定 GitHub ref 安裝是既有公開介面，不增加 evaluator 服務。

- 修正前／後皆用 Codex 原生 discovery 驗證完整名稱是否碰撞；不能以翻譯結果相同反推用了哪個來源。
- 明確選取使用 host 回傳的 name／path，檢查 host 回傳的 userMessage 確認收到該選取；自然語言指定來源另外記錄實際讀取的 skill 路徑。
- 驗證翻譯、指定例句數、管理負例，以及同一 thread 的準備、作答、自修、來源比較、新情境和準確收尾。
- 先前兩份逾時紀錄已查得 429 限流及 562／420 秒重試等待。本次記錄 transport 狀態並尊重退避；不將逾時當作語言行為失敗或通過。
- 自動自然語言選用沒有來源要求時，可選到任一適用來源；這與要求 alpha 卻讀取 GitHub 的情況分開判斷。

## Completion

來源／帳號封裝檢查與測試通過；帳號讀回只剩三份 alpha skill；GitHub 新 ref 的個人安裝內容與來源一致；兩來源 discovery 無同名碰撞；記錄已完成的模型行為與限制。雙軸 review 無未處理的重要問題。

不以 CLI／app-server 結果宣稱已手動驗證桌面 `@` 下拉選單，也不保證所有未測過的自然語言要求都不會誤選。公開 tag 與 GitHub Release 不在這次固定 commit 更新流程中。
