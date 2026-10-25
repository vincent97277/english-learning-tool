# 哪份最小初版規格已足以交付實作？

Type: grilling
Labels: wayfinder:grilling
Status: claimed
Assignee: vincent97277
Parent: ../map.md
Blocked by: 01, 02, 03, 04

## Question

將研究與已確認行為收斂為可直接實作的規格，與使用者確認最小檔案結構、兩個平台的安裝與調用入口、必要驗收案例、Git／發布流程及明確不做的事項。哪些仍未實測的相容性事項必須列為實作階段的驗收門檻，而不能寫成已支援？規格保存為同目錄上層的 `spec.md`，細節以相關決策票為準。

## Context

研究答案分別見[雙平台調用與封裝](01-platform-invocation.md)、[既有行為 review](02-existing-skills-review.md)、[Git 與版本流程](03-git-workflow.md)。需在規格中明列：候選雙 manifest、GitHub 安裝所需 catalog、Codex selector 實際名稱、兩平台安裝／更新／固定 ref、舊 plugin 並存與正反觸發案例。官方文件查核不能代替這些實測，也不需要為了寫規格提前安裝或發布。

## Assets

- [初版規格草案](../spec.md)：待使用者確認，尚未作為實作授權或已驗收聲明。

## Comments

2026-10-26：已完成可審閱草案。提案採 `english-learning-tool` 一包兩個 skill、共用內容與各平台必要封裝；保留已確認輸出，將 discovery、明確調用、舊 plugin 並存與固定 ref 列為實作驗收門檻；Git 流程依研究採初版 main、後續短命分支與 PR。待使用者確認是否以整份草案作實作依據；未確認前維持 claimed，不記 resolution。
