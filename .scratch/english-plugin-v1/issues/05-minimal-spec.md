# 哪份最小初版規格已足以交付實作？

Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: vincent97277
Parent: ../map.md
Blocked by: 01, 02, 03, 04

## Question

將研究與已確認行為收斂為可直接實作的規格，與使用者確認最小檔案結構、兩個平台的安裝與調用入口、必要驗收案例、Git／發布流程及明確不做的事項。哪些仍未實測的相容性事項必須列為實作階段的驗收門檻，而不能寫成已支援？規格保存為同目錄上層的 `spec.md`，細節以相關決策票為準。

## Context

研究答案分別見[雙平台調用與封裝](01-platform-invocation.md)、[既有行為 review](02-existing-skills-review.md)、[Git 與版本流程](03-git-workflow.md)。需在規格中明列：候選雙 manifest、GitHub 安裝所需 catalog、Codex selector 實際名稱、兩平台安裝／更新／固定 ref、舊 plugin 並存與正反觸發案例。官方文件查核不能代替這些實測，也不需要為了寫規格提前安裝或發布。

## Assets

- [已確認的初版規格](../spec.md)：後續實作依據，平台驗收仍須實際執行。

## Comments

2026-10-26：已完成可審閱草案。提案採 `english-learning-tool` 一包兩個 skill、共用內容與各平台必要封裝；保留已確認輸出，將 discovery、明確調用、舊 plugin 並存與固定 ref 列為實作驗收門檻；Git 流程依研究採初版 main、後續短命分支與 PR。待使用者確認是否以整份草案作實作依據；未確認前維持 claimed，不記 resolution。

## Answer

2026-10-26：在展示具體草案並詢問是否採用後，使用者回覆「Next」；依對話上下文確認採用該草案，規格標記為已確認。本票完成，Wayfinder 的研究與初版規格目的地已達成。

採納的實作依據為上方連結的 `spec.md`：一包兩個獨立 skill、共用內容與必要平台封裝；保留已確認輸出契約；採初版 main、發布後短命分支與 PR、固定版本來源的維護流程。所有平台載入、調用、舊 plugin 並存與固定 ref 的實測，留作實作階段的完成條件。

本次結案完成的是規劃，不把規格確認記成 plugin 已實作、安裝、驗收或發布，也不因此改動既有已安裝 plugin。
