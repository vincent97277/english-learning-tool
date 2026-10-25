# 小型 skills plugin 的 Git 與版本流程研究

研究日期：2026-10-26。範圍：單人維護、公開 MIT 授權、Claude Code 與 Codex 共用的英語 skills plugin。這是研究建議，不代表分支保護、版本發布或安裝驗證已完成。

## 建議決策

採用一條 `main` 加上短命工作分支，發布時建立固定 `v0.x.y` tag。初版依既有授權可直接在 `main` 製作；首次發布後，會改變 skill 行為、識別名稱、manifest、安裝方式或版本的工作，先開短命分支並用簡短 PR 留下變更與驗證紀錄。純文字錯字且不改變語義，可直接提交 `main`。不設 `develop`，不常設 release branch，也不為兩個 skills 加上完整 CI 或自動發版系統。

這是對本專案成本的判斷。官方 GitHub flow 提供輕量的「分支 → 提交 → PR → 合併」流程；分支能把尚未合併的工作與預設分支隔開，PR 則提供回饋與 review 空間。單人專案不需要為了形式要求另一位核准者。來源：[GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)。

## 選項與取捨

| 選項 | 成本與用途 | 本專案判斷 |
| --- | --- | --- |
| 全部直接提交 `main` | 操作最少；每次提交立即成為主線，較少自然的 review 節點 | 初版可用；後續只保留給小型文件修正 |
| `main` + 短命 feature/fix 分支 | 在合併前集中比較、驗證與撤回一組變更 | 採用；工作隔離有具體收益 |
| 長期整合分支、多層穩定分支 | 能支援不同成熟度或多條維護線，也增加同步負擔 | 現在沒有需求，不引入 |

Git 官方說明長期分支與 topic branch 都是可用模式，topic branch 適合單一功能或相關工作；並非每個專案都必須同時採用多層長期分支。以上取捨是依規模做出的推薦，不是 Git 規範要求。來源：[Git — Branching Workflows](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)。

## 開發與合併規則

1. 從最新 `main` 建立描述清楚的分支，例如 `feat/translation-input`、`fix/pattern-trigger`。每個分支只處理一組相關變更，提交保持可理解、可回復。
2. 在分支上修改，完成與變更相關的檢查；不用為一個拼字修正建立測試框架。
3. 會影響使用體驗的變更開簡短 PR：說明原問題、改後行為、驗證結果及未驗證項目。單人可自我 review 與合併；這能留下公開維護紀錄，但不是獨立第二人審查。
4. 合併門檻：diff 只含預期檔案；無私人內容；manifest/skill 格式有效；既有「明確調用」與受影響的自動辨識情境通過；跨平台宣稱有相對應證據；如有發布，版本與變更紀錄一致。未測平台必須明列，不能當成已通過。
5. 合併後刪除已完成分支。預設用 squash merge 保留一筆完整變更；若分支內每筆 commit 各自有保留價值，也可一般 merge，不制定額外歷史潔癖規則。

分支、獨立完整提交、PR、合併與刪除分支的基本步驟來自 [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)；上述合併門檻與 squash 偏好是本專案提案。第一版可把門檻寫入簡短的貢獻說明，先靠維護者執行；有反覆漏檢再補小型自動檢查。

分支保護是另一層「強制執行」。公開 repo 的 GitHub Free 可使用 protected branches，規則能限制 force push/刪除並要求 PR 或 status checks。本案可在首次發布後只保護 `main` 的刪除與 force push；是否強制 PR 留到多人協作或確有繞過問題時再開，避免純文件修正也被迫繞流程。尚未建立的 CI 不列為 required checks，也不要求單人無法取得的第二人核准。這些均未設定。來源：[About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)。

## 主線、發布與安裝者的版本隔離

`main` 代表下一版的工作整合結果；發布版本用 tag 指向已驗證的提交。只要不移動舊 tag，未來提交 `main` 不會改變該 tag 指向的內容。發布採 annotated tag，例如 `v0.1.0`，附上發布訊息；Git 官方建議正式標記使用 annotated tags，它會保存標記者、日期與訊息。來源：[Git — Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)。

GitHub Release 以 tag 為基礎，可以附 release notes，並提供該 tag 的 ZIP/tarball。初版無二進位產物時，tag 加 Release 與簡短說明已足夠，不必另外製作多份重複壓縮包。來源：[About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)。

**有 tag 不等於安裝者已隔離。** 如果平台安裝來源仍追蹤 `main`，更新時仍可能取得主線新內容。推薦安裝說明使用平台確實支援的固定 tag、commit ref 或指定發布產物；開發用安裝才追蹤 `main`。兩平台支援的實際設定與更新行為須由平台研究及安裝測試確認，本報告不宣稱任一平台的 plugin 安裝指令已驗證。這是由 Git 的 ref 行為推導的安裝要求。

Git tag 本身仍可被人重設，不能把它稱為技術上不可變。建議首次正式發布前啟用 GitHub release immutability，先建立 draft、放齊資產再發布；官方機制會鎖住發布關聯的 tag 與資產。若暫不啟用，也必須遵守「已發布 tag 不搬動，修正另發版」的維護約定。此設定尚未實施。來源：[Immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)、[Preventing changes to your releases](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes)。

## 版本與變更紀錄

初次可用版本以 `0.1.0` 開始。SemVer 把 `0.y.z` 定義為初期開發、公開介面尚未穩定；已發布版本的內容不能直接改掉，任何修改要另發新版本。`1.0.0` 之後才套用規範對 major/minor/patch 的正式相容性要求。來源：[Semantic Versioning 2.0.0](https://semver.org/)。

本案另外約定 pre-1.0 的簡單溝通方式：

- `0.y.z → 0.y.(z+1)`：修復既定行為、等義文字修正，不改 skill 名稱、調用方式或輸入輸出承諾。
- `0.y.z → 0.(y+1).0`：新增能力、調整可觀察行為或任何不相容改動。若會破壞既有使用方式，release notes 顯著標示並提供遷移例子。
- `1.0.0`：兩平台支持範圍、公開識別名稱、調用方式及主要行為已可承諾穩定時再發布。

這個 `0.x` patch/minor 分工是專案自訂承諾，並非宣稱 SemVer 強制 `0.x` 一定如此。skill 專案的「公開介面」應先用 README 說清楚：plugin/skill 識別名稱、支援平台、明確調用方式、接受的輸入與主要輸出行為；不承諾模型每次產生逐字一致的句子。

版本只維護一套。優先以產品必需的主要 plugin manifest 之 `version` 為權威；若 Claude Code 與 Codex 都要求宣告版本，其他 manifest 與 marketplace entry 是同一版本的副本，發版前核對全部相同、tag 的 `v` 去掉後也相同。不為了儲存版本另外引入 npm、獨立 `VERSION` 或生成工具。主要 manifest 的確切位置由跨平台封裝研究決定；若最終沒有任何 manifest 要求版本，tag 即為權威。這是本案推薦的避免漂移方案。

維護一份 `CHANGELOG.md`：未發布內容放 `Unreleased`，發版時記上版本、日期及使用者可感受到的改變，必要時附不相容改動與未驗證限制。Release notes 摘取該區塊，不再維護另一份不同內容。只改研究文件或貢獻說明可不發產品版本。GitHub 也支援自動生成 release notes，但兩個 skills 初版手寫數行更容易說清楚行為。來源：[About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)；檔案形式與更新時機為專案建議。

## 何時才新增舊版維護分支

預設只支援最新發布版；舊 tag 保留供回查或回退，不代表每個版本都有維護線。只有當 `main` 已含無法一起發布的新版改動，且使用者確實需要舊版的重要修復時，才從該舊 tag 建 `release/0.y`，只回補修正、發 `0.y.(z+1)`，並把適用修正帶回 `main`。沒有人依賴或無後續修補需求時不用常駐該分支。這是 Git topic/long-running branch 模型在本案的最小使用方式，不是官方要求每次發布都建 release branch。來源：[Git — Branching Workflows](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)。

## 公開追蹤的內容邊界

追蹤可重用產品內容、manifest、MIT `LICENSE`、去識別化範例與維護文件。排除憑證、私人設定、真實學習紀錄/對話輸出、安裝快取、暫存研究素材及本機工具產物。不要為了排除私人設定而忽略整個平台目錄，否則可能連需要發布的 manifest 也排除。

`.gitignore` 範本應依實際檔案形狀收斂，例如：

```gitignore
# Credentials and local environment; a sanitized example may be committed
.env
.env.*
!.env.example
*.pem
*.key

# Local work and generated content
.cache/
node_modules/
__pycache__/
*.py[cod]
.DS_Store
```

本 repo 的 `.scratch/english-plugin-v1/` 是經審查可公開、已納入追蹤的 canonical map 與 decision tickets，不忽略整個 `.scratch/`；私人暫存不放在這裡。也不先忽略通用的 `output/`、`logs/` 或整個 `.claude/`、`.codex/`：若未定義用途，可能誤排產品資料。日後若確有本機學習輸出，另外命名並排除對應資料夾。開發者個人 editor/工具差異可放 `.git/info/exclude` 或全域 ignore；所有協作者都需要的排除才放 repo 的 `.gitignore`。官方明確指出 ignore 只影響未追蹤檔案；已追蹤檔案須先 `git rm --cached -- <path>` 才停止未來追蹤，過去提交仍保留內容。來源：[gitignore](https://git-scm.com/docs/gitignore)。

最低人工確認是在每次公開 push 前讀 `git status --short`、`git diff --cached` 與預定提交的檔名；要確認忽略原因可用 `git check-ignore -v -- <path>`。應明確 stage 預期檔案，避免把整個安裝環境複製後直接全部加入。`--cached` diff 比較暫存內容與提交，`check-ignore` 可解釋 ignore 規則；這些檢查不是完整秘密掃描。來源：[git-diff](https://git-scm.com/docs/git-diff)、[git-check-ignore](https://git-scm.com/docs/git-check-ignore)。

GitHub 對公開 repo 的使用者 push protection 預設開啟，可作額外防線，但本案未讀取帳戶實際設定，也未測試攔截。來源：[Managing push protection for users](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/prevent-future-leaks/manage-user-push-protection)。若真的洩漏 token/password，先撤銷或輪替；必要時再依官方流程協調清理歷史、fork/clone 與快取，單刪檔或加 ignore 不能使已公開的秘密失效。來源：[Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)。本研究未發現或宣稱有秘密洩漏。

## 本次研究工作與產品流程的區別

Wayfinder 的研究筆記發布到 `research/git-workflow` 分支：只推研究結果、不開 PR、不合併產品主線。這是本次研究證據的保留方式，不是未來產品 feature/fix 的開發政策；規格完成後才把正式維護規則納入產品文件。

已完成：官方文件查核、流程比較與本提案。未完成：plugin 實作、兩平台安裝/固定 ref/更新實測、manifest 一致性檢查程式、branch/tag protection、release immutability、CI、版本 tag/Release 發布、完整 Git 歷史敏感資料稽核。這些未完成事項不影響研究結論，但產品發布時必須用實際結果替換相關假設。
