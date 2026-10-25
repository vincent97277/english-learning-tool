# 翻譯載入與行為驗收

日期：2026-10-26。範圍：翻譯工單的開發實作，未發布 tag 或 Release。測試僅使用合成文字；個人安裝與設定未修改。此表記錄實際觀察，格式檢查與 discovery 不代表語言行為已通過。

## 主要驗證邊界

客戶端載入 plugin → 選取 skill → 使用者可見輸出。原 repo 沒有測試框架；本次沒有新增鏡像單元測試或模型評分服務。

Red：基底 commit `f5d331c` 沒有 plugin manifest 或翻譯 skill，新整合 plugin 無從載入。

Green：新增最小封裝與改善後的 skill，實際客戶端結果如下。

| 客戶端 | Discovery／載入 | 明確入口 | 行為結果與限制 |
| --- | --- | --- | --- |
| Codex CLI 0.162.1 | 隔離設定下 marketplace add、list available、plugin add 成功；app-server skills/list 無錯誤，回傳 enabled skill 與 plugin ID | `$english-learning-tool:english-translator` | 從空的暫存工作目錄執行，合成案例結果見下表。沒有從 prompt 貼入 skill 本文。 |
| Claude Code CLI 2.1.310 | 隔離設定下 validate、marketplace add、install、list 成功，狀態 enabled；啟動的 skills 與 slash_commands 均列出本 skill | `/english-learning-tool:english-translator`（啟動清單確認） | 發送該入口後停在 `Not logged in`。尚未觀察到翻譯輸出；認證是外部阻礙。 |
| 目前使用的 Codex 桌面 | 未執行 | 待 selector 實測 | 未驗證桌面安裝、選取、輸出與舊 plugin 並存，不以 CLI 代替。 |

測試來源是當前實作 checkout；Codex 安裝後從隔離快取載入。這是可變開發來源，**不是固定版本或更新驗收**。portable 根 manifest 已被 CLI 正確辨識，未增加相容 manifest。Claude validate 最後通過；僅有與公開目錄提交相關的缺圖示警告，本階段不提交目錄、不搬移舊圖示。

## Codex CLI 可見行為

每個案例以新隔離 session 執行；除明確入口以外的案例只送下列普通訊息。人工檢查外部結果，不比對逐字固定答案。

| 案例 | 合成輸入 | 實際觀察 |
| --- | --- | --- |
| 明確翻譯 | 選 Translator，加「我可能會晚 10 分鐘，但還沒確定；請不要等我。」 | 三個標題 Spoken、Direct Message、Writing；皆保留 10 分鐘、不確定與不要等，無附加講解。 |
| 單版、語氣、引文 | 選 Translator，加「翻成英文，只要一版，正式一點：『請不要刪除這 3 個檔案；我還不確定明天能否完成。』」 | 一版正式英文，保留三個檔案、否定與不確定；沒有執行刪檔工具。 |
| 自動匹配改寫 | `Make this English sound more natural: I look forward to meet you.` | 三版改為自然的 `looking forward to meeting`／`look forward to meeting`，沒有句型課。 |
| 自動匹配翻英 | 「幫我翻成英文，只要一版：我還不確定能不能出席。」 | 一版英文保留未確定出席。 |
| 管理要求負例 | 選 Translator，加「請說明這個 plugin 的觸發規則應該如何改善，簡短回答，不要改檔。」 | 中文提出觸發改善，沒有翻譯要求本身、沒有改檔。 |
| 裸英文負例 | `I went for a walk today.` | 普通對話追問散步，未產生三版翻譯或教學。 |
| 技術問題負例 | `Explain what a Python virtual environment is. Keep it short.` | 簡短技術解答，未套翻譯格式。 |
| 缺素材 | 只選 Translator | 只詢問要翻譯或潤飾的文字。 |
| 其他目標語言 | 選 Translator，加「請翻成繁體中文：See you then.」 | 回覆「到時候見。」，沒有改成英文或強加三版。 |

以上證明特定輸入的可見結果；不宣稱已量化自動選取可靠度，也不保證底層每次一定選用相同路徑。

## 重現

1. 使用 README 的本機載入命令，在選定 checkout 安裝；若需保留原安裝，使用客戶端支援的獨立設定目錄，登入／認證必須由可用授權提供。
2. 開啟新 session。確認清單回傳該 plugin 名稱與獨立 skill namespace；Codex 可透過 app-server `skills/list` 檢查，Claude 可檢查啟動清單。
3. 於空的測試工作目錄，逐項使用上表合成輸入，檢查翻譯是否忠實、版本數是否正確及是否誤觸其他任務。不要把正式學習內容或認證記錄提交到 repo。
4. 每個客戶端各自記錄版本、來源 commit、入口及觀察；缺失能力保留未完成，不用靜態檢查代替。

## 尚待完成

- Claude Code 已登入環境的可見翻譯、正反觸發與續接／換題。
- Codex 桌面 discovery、selector、直接輸出及新舊 plugin 並存。
- 跨回合續接偏好與換題、新舊 plugin 同時啟用下的直接入口。
- 全包雙技能整合與固定版本／更新測試，由後續工單涵蓋。

## 輔助靜態檢查

JSON 與 skill YAML 使用標準 parser 讀取成功；名稱與目錄一致。skill-creator 的 Python validator 因環境缺少 PyYAML 未能執行，已由 YAML parser 和實際 host discovery 補驗格式，未將這些檢查當作行為證據。新增內容已檢查私人絕對路徑、常見憑證模式與 staged diff。
