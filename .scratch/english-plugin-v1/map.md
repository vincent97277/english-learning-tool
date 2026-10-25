# 英語學習 plugin 初版規劃

Type: map
Labels: wayfinder:map

## Destination

完成 English Patterns 與 English Translator 的 review、Claude Code／Codex 個別 skill 調用與封裝研究，以及適合小型公開專案的 Git 流程研究，形成可直接實作的初版規格。本次不遷移或發布 plugin。

## Notes

- 2026-10-26 使用者確認：本次終點為研究與初版規格；精準調用以明確指定各個 skill 為主，自動辨識為輔，不要求必經選單。
- 以 skill 為主；只有明確無法達成目標或代價過高才考慮其他能力。保持通用、簡潔、簡單，避免過度設計。
- 初版以 review 並改善兩項現有功能為主。不得鎖定私人路徑、帳號、資料來源；不得改動現有已安裝 plugin。
- 公開專案，MIT 授權。不得提交憑證、私人學習紀錄、快取、絕對私人路徑或來源不明的圖示資產。一般化例句可用合成內容。
- 採 Wayfinder 與本機 Markdown tracker：每票一檔、`Blocked by` 表示依賴；open、無未解依賴、無 assignee 的子票為 frontier，依編號排序。
- 研究使用 research 技能與背景代理；平台事實以官方文件／原始碼為準，Codex 部分另遵循 OpenAI Docs。研究報告放在各自的 `research/*` 分支，推送但不開 PR、不合併。
- 對話決策使用 grilling／domain-modeling；skill 內容評估參考 skill-creator／writing-for-agents。每次只解一張非研究票，不替使用者回答。
- 本輪只建圖、派發與收錄研究。研究完成後由使用者參與確認行為，再收斂規格。
- 尚未設定外部 issue tracker；依技能預設使用本機 Markdown。若要更換可執行 `/setup-matt-pocock-skills`。

## Decisions so far

<!-- 已解票的簡短索引；詳細答案只放在該票。 -->

## Not yet specified

- 平台實際限制或內容 review 可能揭露的相容性例外，待研究後判斷是否值得納入初版。

## Out of scope

- 本次直接遷移、安裝、上架或發布 plugin。
- 新增其他學習功能、MCP 服務、後端、帳號系統、個人學習資料庫；未證明有需求前不引入路由層或建置系統。
