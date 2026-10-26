# 驗證總覽

日期：2026-10-26。目標 `0.1.0` 的實作與發版資料已備妥；尚未發布 tag 或 GitHub Release，跨客戶端驗收仍有缺口。

主要邊界是「客戶端載入 plugin → 選取或匹配 skill → 檢查使用者可見輸出」。只用合成文字與隔離設定，不改動／停用個人 plugin，不提交認證或真實學習資料。模型結果按意思、輸出契約與任務邊界檢查，不逐字比對，也不承諾自動匹配百分之百正確。

| 執行環境 | 已通過 | 待補 |
| --- | --- | --- |
| Codex CLI 0.162.1，模型回報 `gpt-6.1-sol` | 兩 skill discovery、安裝、明確選取及語言行為；翻譯九個案例、句型／切換及並存十五個案例；固定 GitHub commit、產品 fixture 不漂移與明確切版；新來源／切版後三個最小回歸 | TUI 的 `/skills`／`$` selector 操作未實測；app-server 選取與文字翻譯入口已有證據。沒有已發布正式 tag 可驗收。 |
| Claude Code CLI 2.1.310 | 既有 JSON／封裝驗證、隔離本機 marketplace 安裝、啟動與雙 skill inventory | 使用者沒有 Claude Code，決定本輪暫不測。模型輸出、混合／續問／並存、產品的遠端固定 ref 與更新驗收均未完成；本輪沒有新增登入或模型測試。 |
| Codex 桌面 | 僅提供必要 catalog 與共用 skills；不算桌面通過證據 | 實際安裝、selector、調用、輸出、並存、固定來源及切版均待補。既有工具禁止操作此 app，沒有改用其他路徑繞過。 |

## 詳細紀錄

- [翻譯載入與行為](validation/translation.md)：三版、忠實性、覆寫、素材命令、缺素材及正反觸發。
- [句型與功能切換](validation/patterns-and-switching.md)：預設密度、文法／自然度、局部追問、混合要求、換題與舊 plugin 並存。
- [固定版本與交付](validation/fixed-version-delivery.md)：真實固定 commit、產品內容 fixture 的 refresh／切版、最小回歸與限制。

三份紀錄描述各階段來源；前兩階段是可變開發 checkout，固定來源的結果另見交付紀錄。既有完整行為案例未因文件變更而全量重跑；新來源／更新只執行相關最小回歸。

## 當前交付界線

使用者已同意「先完成實作，保留待補驗收」，並補充「我沒有 claude code，所以可以先不測試」。因此內容整合與下一工單可繼續，但未完成條件保持未勾，三張工單不冒稱全部 resolved。正式規格仍以三個客戶端為支援目標，缺少實測不等於已支援。

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
