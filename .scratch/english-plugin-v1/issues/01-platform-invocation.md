# 兩個平台如何精準調用與封裝個別 skill？

Type: research
Labels: wayfinder:research
Status: resolved
Assignee: vincent97277
Parent: ../map.md
Blocked by: none

## Question

Claude Code 與 Codex 目前各自如何安裝 skill 為主的 plugin、明確指定其中一個 skill，以及依意圖自動觸發？選取 plugin 是否等同於選取特定 skill？哪些語法與 manifest 欄位有官方依據，哪些需要實機驗證？在共用兩份 skill 內容的前提下，最少需要哪些平台專屬檔案，是否真的需要路由 skill？

研究須附可複製的候選調用範例，區分官方文件支持、推論與尚未驗證。不得因為本機已有轉換後快取就推定 Claude Code 相容。

## Assets

- [雙平台封裝與調用研究](https://github.com/vincent97277/english-learning-tool/blob/8b13471e742ce13430f06c2c575913775253fe7b/docs/research/platform-invocation.md)，保存在 `research/platform-invocation`，未開 PR、未合併。

## Answer

2026-10-26：官方資料支持一個 plugin 包含兩個可獨立調用的 skill，無須增加路由 skill。Claude Code 的 plugin skill 指令為 `/<plugin>:<skill>`；Codex CLI 可用 `/skills` 或 `$` 選取，桌面則依介面選取具體 skill。Codex 完整 namespace 拼法仍需 selector 實測，不能把候選字串寫成已驗證指令。

建議共用一份 `skills/`，以根目錄 portable `plugin.json` 加 `.claude-plugin/plugin.json` 作最小候選封裝；只有實測舊版需要才增加 Codex compatibility manifest。交付 GitHub 安裝時還需要相應 marketplace catalog；兩平台 catalog schema 不先假定可共用，也不預先建立產生器。名稱與正式檔案結構留待規格收斂。

文件記載 Claude marketplace 可用 `#ref`、Codex 可用 `--ref` 固定來源；仍須在實作階段驗證安裝、更新與固定版本。報告附候選 manifests、語法與十二個合成案例，全都未在本專案執行。官方文件已查核，不等於本機支援、雙 manifest 共存或自動觸發已驗收。
