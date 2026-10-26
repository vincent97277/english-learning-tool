# 維護與版本流程

本專案以少量 Markdown skills 與平台 metadata 為主，不需要常設 develop 分支、建置系統、完整 CI 或自動發版。

## 日常修改

初版到 `0.1.0` 可在 main 開發；本次依 implement-spec 使用單一整合分支與各工單短命分支。首次發布後，重要行為、安裝、識別或版本變更從 main 開短命 `feat/…` 或 `fix/…`，只做相關修改，確認受影響的外部行為後提交簡短 PR。單人也可自我 review；純錯字可直接 main。預設只維護最新版，真有舊版修補需求再建立維護分支。

PR 說清楚使用者原問題、結果、驗證與限制。先讀實作規格及對應工單，對照 staged diff，排除私人設定、憑證、快取、真實學習資料及私人絕對路徑。研究分支保持歷史參考，不因實作而合併。

## 版本與發布

根 portable manifest 是版本權威；修改時同步 Claude manifest 的名稱、版本、描述與授權。catalog 沒有重複版本欄位；若日後增加，也必須一致。兩個 catalog 始終指向同一 checkout，避免 catalog 固定、plugin 卻另抓浮動 main。

初期版本約定：修復升 patch，新能力或可觀察承諾調整升 minor。準備 `0.1.0` 不代表已發布。正式發布前完成 review、可用客戶端驗證、更新 CHANGELOG 與 Release 說明，逐項保留未驗證環境。尚未完成的驗收不能因改版本號而關閉。

只有取得發布授權後，才在選定且已推送的 commit 建立 annotated tag（例如 `git tag -a v0.1.0 -m 'English Learning Tool 0.1.0' <commit>`），推送這個 tag，再以同一 tag 建立簡短 GitHub Release。公開 tag 永不移動或覆蓋；錯版用新版本修正。不要以 main 或浮動 latest 作可重現安裝承諾。分支保護與 release immutability 本專案尚未啟用，也不是初版必要條件。

Release 只列實際通過的客戶端與已知缺口，不宣稱缺圖示的目錄上架檢查已通過。GitHub Release 與官方 plugin 目錄上架是不同操作，後者不在本次範圍。

## 驗證原則

優先走「客戶端載入 → 選取 skill → 使用者可見輸出」。JSON／frontmatter 格式與版本同步是輔助檢查，不能取代模型行為。重跑受影響情境；沒有新變更、失敗或未解風險時，不反覆跑整套合成案例。固定來源測試用隔離設定與合成 fixture，不移動公開 tag、不修改個人 plugin；清理自己建立的認證副本或連結，保留原始認證。
