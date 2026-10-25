# 哪種 Git 與版本流程足以安全維護這個小型 plugin？

Type: research
Labels: wayfinder:research
Status: claimed
Assignee: vincent97277
Parent: ../map.md
Blocked by: none

## Question

比較適合單人、小型、公開、skills 為主專案的簡單 Git 流程，提出足以保護已發布版本而不增加過多負擔的建議。須涵蓋初版可直接 main、後續變更分支與合併條件、tag／版本號／changelog、修補舊版本的觸發條件，以及敏感資訊在追蹤與發布前如何排除。以 Git、GitHub、SemVer 與相關平台官方來源為依據，不預設採用 Gitflow、長期 develop 分支或複雜 CI。

區分可由流程保證的事項與仍需測試／人工操作的事項；不可宣稱分支本身能保護使用者已安裝版本。

## Assets

- 預定報告：`research/git-workflow` 分支的 `docs/research/git-workflow.md`。
