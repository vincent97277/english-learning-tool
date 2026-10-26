# English Learning Tool 0.1.0 — Release 草稿

狀態：發版準備，尚未發布。此文件不授權建立 tag、Release 或上架目錄。

## 提供內容

以一個 MIT 授權 plugin 提供 `english-translator`、`english-patterns` 兩個獨立入口。翻譯預設 Spoken、Direct Message、Writing 三版；完整句型講解預設 1–3 個主要句型，各至少三個附中文意思的例句。使用者指定單版、詳略、例句數量時優先遵從。

共用 skills 與最少平台封裝；沒有 MCP、學習資料庫、路由 skill 或私人輸出目錄。

## 驗證與已知限制

Codex CLI 0.162.1 的隔離載入、合成語言案例、舊插件並存與固定來源驗證已有紀錄。app-server 的明確選取不等於 TUI／桌面 selector 已測。Claude Code 2.1.310 僅完成既有封裝、本機安裝與 inventory；使用者沒有 Claude Code，本輪暫不測其語言與產品更新 lifecycle。Codex 桌面實際安裝、selector、輸出、並存及切版待補。

各項結果與範圍見[驗證總覽](verification.md)。目前保留平台驗收未完成，不能宣稱三客戶端完整支援。

## 發布前

- [ ] 整合分支完成 review，已確認內容合併至選定的發布 commit。
- [ ] 評估並補齊目標平台驗收；缺口若保留，發布範圍與工單狀態須如實反映。
- [ ] 根與 Claude manifest 的版本／識別／MIT 一致，公開 diff 無私人資料或來源不明資產。
- [ ] 將 CHANGELOG 的未發布內容移至正式 `0.1.0` 項目，填上實際日期與 commit。
- [ ] 取得發布授權後，建立並推送不可移動的 annotated `v0.1.0` tag，Release 指向相同 commit。
- [ ] 使用正式 tag 重做必要安裝 smoke，README 的固定開發 commit 改為已驗證的正式 tag；不能提前假定候選 tag 已可安裝。

[安裝與更新](../README.md)目前使用真實存在的固定開發 commit。切換 ref 不能直接對同名來源 re-add；移除 marketplace 影響其全部 plugin。Release 使用者應先閱讀該限制，再決定遷移。
