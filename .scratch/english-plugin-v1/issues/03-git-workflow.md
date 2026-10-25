# 哪種 Git 與版本流程足以安全維護這個小型 plugin？

Type: research
Labels: wayfinder:research
Status: resolved
Assignee: vincent97277
Parent: ../map.md
Blocked by: none

## Question

比較適合單人、小型、公開、skills 為主專案的簡單 Git 流程，提出足以保護已發布版本而不增加過多負擔的建議。須涵蓋初版可直接 main、後續變更分支與合併條件、tag／版本號／changelog、修補舊版本的觸發條件，以及敏感資訊在追蹤與發布前如何排除。以 Git、GitHub、SemVer 與相關平台官方來源為依據，不預設採用 Gitflow、長期 develop 分支或複雜 CI。

區分可由流程保證的事項與仍需測試／人工操作的事項；不可宣稱分支本身能保護使用者已安裝版本。

## Assets

- [Git 與版本流程研究](https://github.com/vincent97277/english-learning-tool/blob/33379717be88e86d6b9e5f446a9668d7e0aec417/docs/research/git-workflow.md)，保存在 `research/git-workflow`，未開 PR、未合併。

## Answer

2026-10-26：已完成 Git、GitHub 與 SemVer 一手資料研究。推薦初版依授權可直接 main；首次發布後，影響行為／安裝／版本的變更用短命分支與簡短 PR，單人可自我 review；純錯字可 main。不引入 develop、常設版本分支或完整 CI。只有真實的舊版修補需求才另開維護分支。

版本隔離依靠固定 tag／commit 與平台實際安裝來源，不是分支名稱。推薦從 0.1.0、固定 annotated tag、簡短 changelog 與 Release 起步；不得移動已發布 tag。pre-1.0 patch／minor 的行為約定為專案提案，不是 SemVer 強制規定。正式採用的流程與必要 manifest 版本欄位在[哪份最小初版規格已足以交付實作？](05-minimal-spec.md)收斂。

公開推送前檢查預期檔名與 staged diff；ignore 不會清除已追蹤內容或歷史。此 repo 的 `.scratch/english-plugin-v1/` 是可公開的 canonical tracker，不能一律忽略。未設定分支保護、release immutability 或 CI，也未進行平台固定版本安裝／更新實測或完整歷史秘密稽核。
