# 來源隔離、完整練習與 GitHub 更新驗收

日期：2026-10-27。依[本輪規格](../../.scratch/source-isolation-20261027/spec.md)，review 基準為 `1d92516`。本文將候選封裝、隔離驗收及正式安裝分開記錄。

## 已確認結果

- 先前兩份未完成驗證的 transport log 顯示 HTTP 429，要求約 562／420 秒重試等待，長於當時的 90 秒截止時間。這是已查得的環境限流證據，不能把原逾時回合改列為行為通過。
- 新驗證工具記錄 transport 狀態、依 thread／turn ID 配對事件，保留先於 RPC 回覆到達的通知，並允許服務退避等待。控制對話同一 thread 的 CONTROL_ONE／CONTROL_TWO 均 completed。
- 修正前，以帳號 0.1.3 與候選 GitHub 0.1.2 同時安裝，原生 `skills/list` 列出 6 個 enabled 入口、3 組完整名稱碰撞；唯一名稱檢查非零失敗。
- 新 `account-source` 產生三個 `*-alpha` 目錄及同名 frontmatter，保留原技能正文與 package 身分。以該帳號候選 0.1.4 與 GitHub 候選 0.1.2 同時安裝，原生 discovery 列出 6 個唯一 enabled 名稱，碰撞為 0。
- CLI 回歸測試先在命令不存在時失敗，實作後通過；另一測試先重現從 alpha 再產生 alpha-alpha 的誤用，加入拒絕規則後通過。原 repo 的檔案內容保持不變，帳號副本可封裝並檢查實際 ZIP。

## 模型驗收方法

使用 Codex CLI 0.162.1／模型回報 gpt-6.1-sol。兩份來源各以無 alpha／GitHub 提示的 `registry-a`／`registry-b` local marketplace 安裝到隔離設定；內容取自實際帳號來源或本輪候選來源。它們不是正式 remote marketplace 的生命週期測試。

使用空工作目錄、ephemeral、read-only、approval never。測試子程序不繼承桌面 task identity／工具 bridge，停用 apps 與 remote_plugin，僅測試已安裝的本機副本；正式帳號與 GitHub 安裝另外驗證。暫存登入連結結束移除，原認證保留。

明確選取傳入 discovery 的 name／path，檢查 host 回傳 userMessage 也包含該 name／path，作為來源證據；不以模型自述或兩個相同翻譯反推來源。自然語言指定來源另外檢查實際讀檔命令。所有輸入均為合成材料。

目前前五個模型回合 completed：GitHub 單版翻譯、alpha 指定兩例句講解、純文字指定 alpha 的翻譯（觀察到讀取 english-translator-alpha）、管理負例，以及 GitHub 回譯出題。後續實際作答遇到 429／約 552 秒退避，正在等待服務重試，尚未列為通過。

## 部署狀態

帳號 0.1.4 候選 ZIP 已通過來源與實際 ZIP 比對；目前正式帳號仍為 0.1.3，尚未把候選的零碰撞結果當作正式帳號已部署。GitHub 新固定 commit、個人安裝與雙軸 review 尚待完成。

原生桌面 `@` 選單的點選操作未手動驗證。自動自然語言意圖辨識的未測情境不作零誤用保證；本輪能檢查的是名稱碰撞、指定來源、任務邊界與實際多回合行為。
