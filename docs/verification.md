# 驗證總覽

2026-10-27：GitHub 0.1.2 已推送並套用個人 Codex 固定安裝 `8e9abb2`，三個 skill enabled；來源快照與安裝快取的五個封裝檔案均與 commit 相符。帳號已更新為 English Learning Tool-alpha 0.1.4，三個 skill 名稱及目錄加上 `-alpha`，舊路徑已移除；帳號完整讀回及實際安裝快取比對通過，正式個人 discovery 六個入口 enabled、名稱碰撞為零。本輪 14 項測試、遠端 CI 與兩軸 review 已完成，最新模型行為與限制以[來源隔離驗收](validation/source-isolation-2026-10-27.md)為準。

以下保留 2026-10-26 的各平台歷史結果，不表示新版入口均已在各平台通過。
日期：2026-10-26。`0.1.0` 已套用 Codex 個人環境與 ChatGPT 私人帳號，兩個舊插件已解除安裝；尚未發布公開 tag 或 GitHub Release，跨客戶端驗收仍有缺口。

後續私人帳號修訂 `0.1.1` 已更新工具集合描述；JSON／YAML、manifest 一致性、實際 ZIP 與安全帳號比對共 11 項回歸通過，帳號讀回無非預期差異、無缺檔。已新增輕量 CI 工作，但尚未推送觸發 GitHub Actions；本機執行相同命令通過。兩份 skill 未變，未重跑模型案例；Codex CLI 的固定來源仍為既有 `0.1.0` commit。

主要邊界是「客戶端載入 plugin → 選取或匹配 skill → 檢查使用者可見輸出」。前期使用隔離設定；本次依使用者授權安裝個人環境與私人帳號版，核心測試通過後解除安裝兩個舊插件。所有案例只用合成文字，不提交認證或真實學習資料。模型結果按意思、輸出契約與任務邊界檢查，不逐字比對，也不承諾自動匹配百分之百正確。

| 執行環境 | 已通過 | 待補 |
| --- | --- | --- |
| Codex CLI 0.162.1，模型回報 `gpt-6.1-sol` | 兩 skill discovery、安裝、明確選取及語言行為；翻譯九個案例、句型／切換及並存十五個案例；固定 GitHub commit、產品 fixture 不漂移與明確切版；新來源／切版後三個最小回歸 | TUI 的 `/skills`／`$` selector 操作未實測；app-server 選取與文字翻譯入口已有證據。沒有已發布正式 tag 可驗收。 |
| Codex CLI 0.162.1，個人設定環境 | 固定 commit 安裝 0.1.0，兩 skill enabled、discovery errors=[]；安裝內容與 repo 相同；以 app-server 的 ephemeral、read-only 工作階段完成翻譯、句型與混合要求三案 | 此列不替代 Codex 桌面 selector 與輸出驗收。 |
| ChatGPT 網頁，私人帳號版 0.1.0 | 帳號儲存及讀回兩份 skill 與 repo 相同；管理頁兩 skill 開啟；選取新版 plugin 後完成三版翻譯、繁中講解且恰兩個例句、單版混合要求三案；兩舊插件解除安裝並重新整理清單確認消失 | 同一對話的三個合成案例，並非全部觸發矩陣；手機與 ChatGPT 桌面 Chat 未測。 |
| Claude Code CLI 2.1.310 | 既有 JSON／封裝驗證、隔離本機 marketplace 安裝、啟動與雙 skill inventory | 使用者沒有 Claude Code，決定本輪暫不測。模型輸出、混合／續問／並存、產品的遠端固定 ref 與更新驗收均未完成；本輪沒有新增登入或模型測試。 |
| Codex 桌面 | 僅提供必要 catalog 與共用 skills；不算桌面通過證據 | 實際安裝、selector、調用、輸出、並存、固定來源及切版均待補。既有工具禁止操作此 app，沒有改用其他路徑繞過。 |

## 詳細紀錄

- [翻譯載入與行為](validation/translation.md)：三版、忠實性、覆寫、素材命令、缺素材及正反觸發。
- [句型與功能切換](validation/patterns-and-switching.md)：預設密度、文法／自然度、局部追問、混合要求、換題與舊 plugin 並存。
- [固定版本與交付](validation/fixed-version-delivery.md)：真實固定 commit、產品內容 fixture 的 refresh／切版、最小回歸與限制。
- [個人環境套用](validation/personal-deployment.md)：Codex 個人環境、ChatGPT 私人帳號版與舊插件移除。
- [英文回譯遷移](validation/back-translation.md)：`0.1.2` 新入口的內容改善、逐輪練習及相關回歸；與上述舊版結果分開記錄。
- [來源隔離與 GitHub 更新](validation/source-isolation-2026-10-27.md)：2026-10-27 的實際個人碰撞、alpha 候選、模型回合、review 與固定安裝更新。
- [alpha 與 GitHub 並存選用](validation/alpha-source-selection.md)：顯示名稱後綴不能消除完整 skill 名稱碰撞；隔離模型案例與來源辨識限制。

三份紀錄描述各階段來源；前兩階段是可變開發 checkout，固定來源的結果另見交付紀錄。既有完整行為案例未因文件變更而全量重跑；新來源／更新只執行相關最小回歸。

## 當前交付界線

使用者先前同意「先完成實作，保留待補驗收」，並補充「我沒有 claude code，所以可以先不測試」；之後明確要求套用 Codex／ChatGPT，測試通過後下架舊 plugin。本次完成私人帳號與個人 CLI 套用及舊版解除安裝，Codex 桌面與 Claude 未完成條件仍保持未勾，三張工單不冒稱全部 resolved。正式規格仍以三個客戶端為支援目標，缺少實測不等於已支援。

正式發布前依 [Release 草稿](release-0.1.0.md)審視缺口與發布範圍；本輪沒有建立／移動公開 tag、建立 GitHub Release 或上架官方目錄。

## Standards

2026-10-26：獨立 review `f5d331c…5609419` 的完整實作 diff，**0 findings**。

- 已對照正式規格、已確認的初版與行為規格、README、維護流程，以及 skill-creator／writing-for-agents 指引。
- 兩個 skill 保持通用、命名清楚、正文精簡，沒有私人路徑、固定帳號、學習資料儲存或非必要抽象。
- 共用內容配上必要雙平台 metadata 符合明訂的最小封裝；少量欄位同步與共通邊界規則不需要額外生成器或共享框架。
- 文件區分開發 commit、未發布版本與固定 tag，沒有將待補驗收寫成通過；未發現值得提出的 Fowler baseline smell。

## Spec

2026-10-26：另一個獨立 reviewer 對照同一 diff、正式規格、三張工單與驗收原始摘要，**0 個可操作問題**。

- 命名、觸發邊界、三版翻譯、講解密度、明示覆寫、混合任務、續問、換題與素材命令邊界均符合已確認要求。
- 兩 manifest 的身分、版本、描述與 MIT 一致；catalog 同 checkout。README 的固定 commit 與目前兩份 skill 的 SHA256 相同。
- 原始安裝／更新 JSON 與公開驗收記錄一致；沒有把本地 fixture 當遠端 lifecycle，也沒有把 app-server 當 TUI／桌面驗收。
- 三張工單保持 in-progress，符合使用者先完成實作、保留驗收的最新安排；沒有增加未要求的學習功能、服務或框架。

兩軸各為 0 findings，無待修正的 review 問題。Review 不替代上表仍未執行的平台驗收；其後僅補上本段交接記錄與規格狀態，未修改 skill 或平台封裝。
