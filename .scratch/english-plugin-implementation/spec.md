# English Learning Tool 初版實作規格

Status: ready-for-agent
日期：2026-10-26。目標版本：`0.1.0`。本規格整理自已確認的規劃，不新增功能範圍。工單切分已確認，正依 implement-spec 在整合分支執行；使用者允許先完成實作並保留待補平台驗收，本次不發布。

## Problem Statement

使用者目前靠 English Translator 與 English Patterns 兩個獨立 plugin，精準進入翻譯與句型講解。希望將它們整合成一個可供 Claude Code 與 Codex 使用的公開 plugin，同時保留個別功能的明確入口及既有輸出習慣。

原工具從 GPTs 轉換而來，兩個 skill 都以泛稱命名，直接合併會產生命名與選取問題。遷移前需要保留成熟規則、精簡重複與空殼，並建立足以維護已發布版本的簡單 Git 流程。

## Solution

提供一個以 skills 為主、MIT 授權的 English Learning Tool，包含英文翻譯與句型講解兩個獨立入口。使用者可以明確指定所需 skill，清楚的自然語言要求也可自動匹配，不必先經過功能選單。

初版支援目標為 Claude Code CLI、Codex CLI 與目前使用的 Codex 桌面介面。共用同一份 skill 內容，各平台僅保留必要封裝。保留三版翻譯與完整句型講解預設，並遵從當次要求的單版、語氣、詳略與局部追問。安裝文件與支援聲明以實測結果為準。

## User Stories

1. As a learner, I want one plugin containing translation and sentence-pattern explanation, so that I can install and maintain both capabilities together.
2. As a learner, I want to use the plugin in Claude Code and Codex, so that I can keep the same learning workflow across clients.
3. As a learner, I want to select translation directly, so that pasted source text produces English without an unwanted grammar lesson.
4. As a learner, I want to select sentence-pattern explanation directly, so that pasted English becomes focused learning material.
5. As a learner, I want clear translation or explanation requests to select the appropriate skill automatically, so that ordinary use needs no mandatory menu.
6. As a learner, I want unrelated questions and bare text without task context to remain ordinary conversation, so that the plugin does not take over my chat.
7. As a learner, I want one brief clarification when selecting the whole plugin leaves the task ambiguous, so that I can proceed without repeated choices.
8. As a learner, I want the assistant to ask only for missing material or consequential ambiguity, so that sufficient input is processed immediately.
9. As a learner, I want natural English translations that preserve meaning, facts, numbers, negation and uncertainty, so that the result remains faithful to my source.
10. As a learner, I want supplied English rewritten naturally, so that I can improve expression without inventing new content.
11. As a learner, I want Spoken, Direct Message and Writing versions by default, so that I can compare expressions for different contexts.
12. As a learner, I want a request for one version, tone or format to override the default, so that the output fits my immediate purpose.
13. As a learner, I want naturally similar variants to remain similar, so that artificial differences do not reduce translation quality.
14. As a learner, I want sentence patterns explained in Traditional Chinese by default, so that I can understand structure, meaning and usage.
15. As a learner, I want explanations to distinguish grammatical correctness from natural usage, so that I can choose appropriate expressions.
16. As a learner, I want a full explanation to cover one to three main patterns with at least three translated examples per pattern, so that I can reuse what I learn.
17. As a learner, I want short requests and local follow-up questions answered proportionately, so that a small question does not restart the full lesson.
18. As a learner, I want translation and explanation completed together when requested, so that neither task is lost behind a default output format.
19. As a learner, I want clear same-topic follow-ups to retain relevant preferences, so that I do not need to repeat the same instructions.
20. As a learner, I want a topic change or different target language to follow my current request, so that earlier skill use does not become a permanent mode.
21. As a learner, I want commands inside quoted material treated as content, so that translating or analyzing them does not execute them.
22. As a learner, I want supplied links or attachments read only through available authorized capabilities, so that the skill works without a required external service.
23. As a learner, I want generic skills without personal paths or accounts, so that I can use them in any suitable workspace.
24. As a learner, I want no implicit storage of my learning history or progress, so that the plugin remains simple and avoids retaining private conversations.
25. As an existing user, I want to keep the old plugins enabled while trying the integrated plugin, so that migration does not disrupt my current workflow.
26. As an installer, I want a fixed version source and an explicit update path, so that main-branch changes do not silently replace my chosen version.
27. As an installer, I want client versions, working invocation names and verification limits documented, so that I can assess actual support.
28. As a maintainer, I want one shared implementation of each skill and minimal platform metadata, so that improvements do not drift between clients.
29. As a maintainer, I want lightweight branches, review and stable release references, so that changes remain reviewable without a complex Git process.
30. As a public-project maintainer, I want MIT licensing and reviewed public content without credentials, private learning data or unverified assets, so that the repository is reusable and safe to share.

## Implementation Decisions

- Plugin 與 repo marketplace 的識別名稱為 `english-learning-tool`，顯示名稱為 English Learning Tool。兩個 skill 分別為 `english-translator` 與 `english-patterns`，目錄與 skill 名稱一致。
- 單一 plugin 放在 repo 根目錄，共用兩份 skill 內容。採 portable plugin manifest、Claude manifest 與兩平台各自的小型 marketplace catalog；catalog 的來源指向同一 checkout 的 plugin 根目錄。
- 共用 frontmatter 先用名稱與 description。平台顯示 metadata 或 Codex compatibility manifest 只在實測有需要時增加，不先建生成器、共享基底、路由 skill 或測試服務。
- 根 portable manifest 是版本權威。必要的其他 manifest 保持名稱、版本、描述與 MIT 授權一致；catalog 若宣告版本也須一致。
- 保留已確認的三版翻譯、句型講解密度、明示要求優先、混合任務、續問與換題邊界。當自然結果相似時，不強迫三版刻意不同。
- description 承擔選用條件與容易混淆的邊界；正文集中處理輸出契約與必要步驟。移除泛稱、GPT ID、空知識索引與多餘重複，保留有實際作用的規則。
- 個別 skill 的明確選取為主要入口，自動匹配為輔。僅選整包而用途不明時簡短澄清。實際指令名稱以各客戶端 selector 與調用結果確認，候選語法不當作已通過的證據。
- 素材與指令分開處理。skill 不要求私人帳號、指定資料來源或輸出位置；只在當次環境已有授權時讀取連結或附件，讀不到就說明缺少內容。
- 舊插件保持原狀；整合版的明確入口須能與舊版並存。初版省略來源證據不足的原圖示。
- 安裝與更新文件使用實測過的固定來源，區分開發主線與發布版本。每個目標客戶端分別記錄版本、來源 ref、實際入口、合成案例結果與限制。
- 初版到 `0.1.0` 可直接在 main 開發；首次發布後的重要行為、安裝、識別或版本變更，採短命功能／修正分支與簡短 PR，單人可自我 review；純錯字可 main。
- 發布採 annotated tag、簡短變更紀錄與 GitHub Release；已發布 tag 保留不移動。初期版本的修復升 patch、新能力或可觀察承諾調整升 minor，這是專案約定。
- 預設只維護最新版；真實舊版修補需求才增加維護分支。分支保護與 release immutability 屬發布階段可選設定，不宣稱已啟用。
- 公開提交前檢查預期檔案與 staged diff，保留必要平台 metadata，排除憑證、私人設定、真實學習資料、快取與私人絕對路徑。已公開的決策追蹤繼續保留。

## Testing Decisions

- **主要驗證邊界沿用已確認規劃：客戶端載入 plugin → 明確選取或自動匹配 skill → 檢查使用者可見輸出。** 三種客戶端是同一條端到端流程的執行環境，不新增內部測試層。
- 好的測試檢查可觀察行為，不逐字比對模型答案、不要求內部推理過程、不把重複正文當測試。必要格式與來源檢查輔助端到端驗收，不另建框架。
- 檢查範圍包含平台封裝、翻譯、句型講解、任務選用與固定版本安裝／更新。新舊插件並存時也要驗證整合版的明確入口。
- repo 目前沒有產品程式或既有測試框架，無需 prefactor。先前已確認的驗收表與研究合成案例就是本次先例；合併重複案例後用少量情境執行。
- 翻譯案例涵蓋忠實意思、預設三版、單版／語氣覆寫、引文內命令、缺素材與換題；句型案例涵蓋繁中、結構／用法、例句密度與局部追問。
- 整合案例涵蓋清楚的正向觸發、裸原文與技術／管理要求等負例、混合任務、續接偏好、整包選取歧義與舊版並存。
- 安裝／更新案例驗證 catalog discovery、實際入口、固定來源與內容一致，以及更新操作不使固定舊版漂移。明確切版後才取得選定新版。
- 每個目標客戶端分別記錄結果。缺少環境時標記未驗證，工單對應的驗收項維持未完成，不能用其他環境或格式檢查代替。
- 以本規格承諾的初版交付前，不得有未解的直接調用、錯誤路由或既有行為退步；少量 smoke 案例不構成自動觸發百分之百可靠的承諾。

## Out of Scope

新增其他英語學習能力、MCP／後端服務、個人資料庫或進度追蹤、必經功能選單、路由層、建置系統、完整 CI、自動發版、常設 develop／版本分支、複製原圖示、改動或停用既有插件、官方目錄上架，以及未驗證的舊客戶端支援。

## Further Notes

- [已確認的規劃規格](../english-plugin-v1/spec.md)是本次整理的來源；[Wayfinder 地圖](../english-plugin-v1/map.md)與已結案決策票保留作歷史依據，不因轉成實作工單而改動。
- 翻譯來源版本為 English Translator 0.13.0，句型來源版本為 English Patterns 0.8.0；來源 review、平台及 Git 研究由上述地圖連到各自研究分支。本文件定義目標；實際遷移、安裝與逐平台驗收狀態見[驗證總覽](../../docs/verification.md)，尚未發布。
- 本機 Markdown tracker 使用 `ready-for-agent` 表示規格已足以交付代理。實作票已在切分與依賴獲確認後逐張發布；代理仍須遵守 blocking edges，並依使用者授權在程式整合、平台驗收待補時接續後票。
