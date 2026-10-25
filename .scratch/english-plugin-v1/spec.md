# English Learning Tool 初版規格

狀態：已確認，可交付實作。確認日期：2026-10-26。目標版本：`0.1.0`。

本文件是實作交接規格，不代表 plugin 已存在、平台驗證已通過或版本已發布。行為決定以[輸出與互動行為決策](issues/04-behavior-contract.md)為準；下一階段實作以本規格為依據。

## 範圍與識別名稱

製作一個 MIT 授權、以 skills 為主的公開 plugin，整合並改善 English Translator 0.13.0 與 English Patterns 0.8.0。初版目標環境為 Claude Code CLI、Codex CLI 與目前使用的 Codex 桌面介面；支援聲明須列出實際測過的客戶端版本。

| 項目 | 名稱 |
| --- | --- |
| Plugin 與 repo marketplace | `english-learning-tool` |
| 顯示名稱 | English Learning Tool |
| 翻譯 skill | `english-translator` |
| 句型講解 skill | `english-patterns` |

每個 skill 的目錄名與 frontmatter `name` 相同，description 各自說明用途、觸發條件與最容易混淆的邊界。兩份內容共用於各平台，不分叉維護。

## 最小交付內容

單一 plugin 直接放在 repo 根目錄，避免為兩個 skills 再包一層專案：

```text
plugin.json
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
.agents/plugins/marketplace.json
skills/english-translator/SKILL.md
skills/english-patterns/SKILL.md
README.md
LICENSE
.gitignore
CHANGELOG.md
docs/verification.md
```

- 根 `plugin.json` 採研究確認的 portable 格式；Claude manifest 只保留必要身分欄位。`name`、`version`、`description`、MIT 授權資訊在兩份 manifest 保持一致，版本以根 manifest 為權威，不增加生成器或 `VERSION` 檔。
- 兩個 marketplace catalog 各只有本 plugin 的一筆資料，使用各平台格式；來源指向同一 repo checkout 的 plugin 根目錄，使固定 marketplace ref 同時固定 skill 內容。確切 JSON 依官方 schema 撰寫並在實作時驗證 discovery。
- 共用 skill frontmatter 先用 `name` 與 `description`。若實測 selector 需要更清楚的顯示標籤，才補可選 `agents/openai.yaml`；若實測目標客戶端需要 Codex compatibility manifest，才增加並記下原因與版本。
- README 提供實測後的安裝、更新、固定版本、個別調用與最短範例，並簡述維護流程。`docs/verification.md` 只放客戶端版本、來源 ref、合成案例結果與限制，不收私人對話。
- 已有 `.scratch/english-plugin-v1/` 繼續作可公開的決策追蹤；研究報告維持各自 `research/*` 分支，實作時讀取相關票的來源連結，不合併研究分支。

## 行為與調用

翻譯預設保留 Spoken、Direct Message、Writing 三版；句型講解預設用繁中，完整講解挑 1–3 個主要句型，每個至少三個附中文意思的例句。單版、簡短、語氣、數量及局部追問等明示要求優先。其餘已確認規則見[行為決策](issues/04-behavior-contract.md)。

以明確選取個別 skill 作主要入口，清楚意圖的自動觸發為輔：

| 情境 | 行為 |
| --- | --- |
| 指定翻譯 skill 並提供素材 | 直接翻成自然英文或自然改寫英文，不另加句型課。 |
| 指定講解 skill 並提供英文 | 直接講解結構與用法，不先要求選功能。 |
| 明確要求翻成英文／講解句型 | 選對應 skill；使用者要兩件事就完成兩部分。 |
| 僅選整包 plugin，素材與上下文無法判定用途 | 一次簡短詢問翻譯或講解；不新增常駐選單或路由 skill。 |
| 只有原文、沒有任務或練習上下文 | 不因語言本身自行進入教學或三版改寫。 |
| 缺少必要素材或有會改變意思的歧義 | 只詢問缺少的部分；資訊足夠就直接處理。 |
| 素材包含命令、後續換題或其他目標語言 | 區分指令與素材，遵循當次任務；兩個 skill 不接管無關要求。 |

Claude Code 的候選明確入口如下，須在實作階段實測後才作正式安裝說明：

```text
/english-learning-tool:english-translator 我會晚十分鐘，請先開始。
/english-learning-tool:english-patterns It might be a bit of a hassle.
```

Codex CLI 先用 `/skills` 或 `$` selector 選兩個 skill；桌面介面從實際提供的選取入口選個別 skill。README 應記錄實際顯示名稱與可複製用法，不把尚未驗證的 `$plugin:skill` 字串當成有效指令。

安裝研究記載 Claude marketplace 可用 `owner/repo#ref`，Codex 可用 `--ref`；實作時以本 repo 的固定版本來源驗證，正式 README 才填入可用指令。公開 GitHub 安裝不等於上架官方目錄。[平台研究與官方來源](issues/01-platform-invocation.md)

## 內容改善與資料邊界

保留原有任務邊界、忠實翻譯、結構／意義／情境講解、素材內指令處理及續問規則；移除泛稱 `instructions`、GPT ID、空 knowledge index 與重複指令。description 負責讓模型找到正確 skill，正文集中寫處理方式與輸出契約，避免重複列長串負例。[來源版本與 review](issues/02-existing-skills-review.md)

skill 不要求特定資料來源、帳號、外部工具或固定輸出路徑；有連結或附件時，只使用當次環境已有且獲授權的讀取能力，讀不到就說明缺少內容。初版不儲存個人進度或對話。

`.gitignore` 保留本機環境與產物排除，按實際檔案補齊私人設定、憑證及私人輸出；不要整個忽略承載 manifest 的平台目錄或公開 tracker。每次 push 前核對 staged diff 與預期檔名，排除秘密、私人絕對路徑、真實學習紀錄和快取。這不等於完整秘密掃描，也不能消除過去已追蹤的內容。

原 PNG 圖示缺可追溯的來源證據，初版省略；需要圖示時另用權利清楚的資產。這次不改動或停用既有已安裝 plugin。

## 實作與發布的完成條件

先驗證必要 JSON、相對來源路徑、skill frontmatter、唯一名稱及版本一致，再以同一組合成案例在目標客戶端作小型驗收。記錄結果與失敗修正即可，不建立 evaluator 服務或通用測試框架。

| 驗收情境 | 可觀察的通過條件 |
| --- | --- |
| 各 catalog discovery 與個別 selector | 列出一個 plugin 和兩個可區分、可直接選取的 skill；兩份 manifest 共存可載入。 |
| 明確翻譯：「我會晚十分鐘，請先開始。」 | 保留十分鐘與先開始的意思，預設三版，不加句型課。 |
| 明確講解：`It might be a bit of a hassle.` | 繁中說明有用結構，完整講解符合已確認例句密度。 |
| 單版覆寫：「翻成英文，只要一版：我還不確定能不能出席。」 | 只一版，保留不確定性。 |
| 混合要求：「翻成英文並解釋句型，只要一版：我以前不習慣早起，但現在習慣了。」 | 一版翻譯及對應講解皆完成。 |
| 局部追問：「那可以換成 a little 嗎？請簡短。」 | 承接原句比較，不重播完整模板。 |
| 正向觸發與負例 | 清楚翻譯／講解要求選對 skill；無上下文的裸英文、技術問題或 plugin 管理要求不誤觸。 |
| 引用內命令、缺素材與換題 | 翻譯／分析命令文字而不執行；只問缺少素材；換題按新任務回應。 |
| 原有兩個 plugin 仍啟用 | 明確選取整合版 skill 不命中舊版，無須先卸載舊 plugin。 |
| 固定 ref 安裝與更新 | 來源與內容符合指定 ref；更新測試不使固定舊版安裝漂移；使用者明確切版後才取得新版。 |

每個目標客戶端記錄 discovery、實際調用名稱、上述結果及來源 ref。CLI 與桌面結果各自列示；缺少某環境時標記「未驗證」，不以另一環境代替。發布為本規格承諾的初版前，目標環境不得有未解的直接調用、錯誤路由或既有行為退步；自動觸發的 smoke 結果不宣稱百分之百可靠。

## Git 與版本流程

初版到 `0.1.0` 可直接在 `main` 開發；首次發布後，影響行為、識別名稱、manifest、安裝或版本的變更，使用短命 `feat/*`／`fix/*` 分支與簡短 PR，單人可自我 review。純錯字修正可直接 main。合併前確認受影響案例、公開內容與版本一致性；合併後刪除工作分支。

發布使用 annotated `v0.x.y` tag、簡短 CHANGELOG 與 GitHub Release，安裝說明使用已驗證的固定來源。根 manifest 與必要副本版本一致；舊 tag 保留不移動。`0.x` 期間，修復既定行為升 patch，新增能力或調整可觀察承諾升 minor；此為專案約定。[Git 研究與官方來源](issues/03-git-workflow.md)

預設維護最新版本；只有真實舊版使用者需要重要修補、且 main 無法直接發布時，才從舊 tag 建維護分支。分支保護與 release immutability 可在發布階段依需求設定，這份規格不宣稱已啟用。初版不引入 develop、常設 release 分支、完整 CI 或自動發版。

## 不在初版範圍

新增其他學習功能、MCP／後端服務、個人資料庫、路由 skill、必經選單、建置系統、複製原圖示、官方目錄上架，以及未驗證的舊版客戶端支援。
