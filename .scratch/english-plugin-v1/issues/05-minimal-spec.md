# 哪份最小初版規格已足以交付實作？

Type: grilling
Labels: wayfinder:grilling
Status: open
Assignee: none
Parent: ../map.md
Blocked by: 01, 02, 03, 04

## Question

將研究與已確認行為收斂為可直接實作的規格，與使用者確認最小檔案結構、兩個平台的安裝與調用入口、必要驗收案例、Git／發布流程及明確不做的事項。哪些仍未實測的相容性事項必須列為實作階段的驗收門檻，而不能寫成已支援？規格保存為同目錄上層的 `spec.md`，細節以相關決策票為準。

## Context

研究答案分別見[雙平台調用與封裝](01-platform-invocation.md)、[既有行為 review](02-existing-skills-review.md)、[Git 與版本流程](03-git-workflow.md)。需在規格中明列：候選雙 manifest、GitHub 安裝所需 catalog、Codex selector 實際名稱、兩平台安裝／更新／固定 ref、舊 plugin 並存與正反觸發案例。官方文件查核不能代替這些實測，也不需要為了寫規格提前安裝或發布。
