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
