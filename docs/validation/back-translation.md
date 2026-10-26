# 英文回譯練習遷移驗證

日期：2026-10-26。來源：本輪 repo checkout，manifest `0.1.2`，未提交／發布。
名稱、完整流程與 repo 實作範圍由使用者確認，見[遷移規格](../../.scratch/back-translation-migration/spec.md)。

## 變更與靜態檢查

只遷移 back-translation-practice 的 runtime，重命名為 `english-back-translation`；保留材料公平性、逐輪等待、每段原文比較、一次新情境、必要／可選修正與準確收尾。補上明確選取、續接、任務切換和素材指令邊界，將 B-depth 設計用語改為具體回饋內容。精簡正文並拆開長行，不另建 references、scripts 或路由層。

兩個現有 skill 只調整整包用途不明時的澄清，涵蓋回譯練習。兩 manifest 版本／描述與 catalog 描述同步；本次依使用者要求升 patch，不改一般新能力升 minor 的約定。

- 既有 `unittest discover -s tests`：11 項通過，未新增正文鏡像測試。
- `scripts/plugin.py check`：通過，3 個 skill、5 個封裝檔案。
- skill-creator 的 `quick_validate.py`：新 skill 通過。
- `scripts/plugin.py pack`：來源與實際 ZIP inventory／內容比對通過，只包含根 manifest、LICENSE、三份 skill。
- `git diff --check`：通過。

## 獨立行為檢查

獨立代理只收到新 skill 路徑與合成使用者輸入／對話，未提供預期答案、實作理由或既有評語。先跑四案，再補一組原句修訂及新情境收尾；逐案產出真實助理回覆，由主代理檢查。這是 skill 指令的行為檢查，不是平台安裝證據。

| 情境 | 可見結果 |
| --- | --- |
| 指定 AI 翻譯後出題 | 對 `I would have called you if I had known you were free.` 只給繁中提示與作答邀請，未提前給完整英文答案。 |
| AI 中文漏掉 `Unless it rains` | 接受學習者依不完整提示寫出的 `We'll meet outside.`，明說中文漏譯，修正材料並比較 unless／if … not，未指責學習者漏寫條件。 |
| 直接求助並結束 | 示範 `didn't … until …`，比較來源中的 `how tired I was`，明確結束並記為示範、未觀察到獨立產出，新情境依要求跳過。 |
| 選 skill 但要求只翻繁中 | 只翻譯 `I might be a little late.`，未開始練習。 |
| 原句修訂後轉新情境 | 接受 `I wish I had left earlier.`，說明其過去後悔含義，接著出「昨天太晚睡」的單一新情境並等待。 |
| 新情境正確後收尾（修正後重驗） | 接受 `I wish I had gone to bed earlier.`，明確完成，指出 had + 過去分詞已教過、這次為有句型支持的運用；將自行選用的 go to bed 另外描述，不宣稱穩定掌握。 |

漏譯修正後，代理接受原答、補充條件、比較來源並進入新情境，符合原流程；沒有強制重做同句的新增承諾。

首次新情境收尾將整句描述為「自行寫出」，協助歸因不夠精確。已補明新情境重用教過的詞語或結構仍算受協助產出，再以同一原始對話重驗，得到上表結果。

## 隔離 Codex 客戶端

Codex CLI 0.162.1，暫存設定根與空工作目錄，本機 marketplace 指向本輪 checkout。透過公開 app-server `skills/list` 取得安裝路徑，明確案例以 `skill` input 選取，自動案例只送一般文字；未把 skill 正文貼入 prompt。工作階段 ephemeral、read-only、approval never；暫存認證連結在測試結束移除，不改個人來源或安裝。

載入已通過：三個獨立入口 enabled、discovery errors 為 0。第一個模型請求在限制網路的執行環境遇到連線中斷，沒有算為通過；以同一隔離設定獲准網路重試。

| 情境 | 可見結果 |
| --- | --- |
| 明確新入口、AI 準備 | `I wish I had left earlier.` 被譯為「要是我當時早一點離開就好了」，接著邀請英文回譯並等待，未先給英文答案。 |
| 同 thread 實際作答 | 收到 `I wish I leave earlier.` 後指出過去後悔及 had + 過去分詞，給一次修正機會並等待，未先貼完整修訂。 |
| 最終來源、自動回譯入口 | 普通訊息「請帶我做回譯練習：I would have helped if I had known.」自動讀取新 skill，詢問自譯或 AI 翻譯並等待。 |
| 最終來源、合成收尾上下文 | 以原始合成對話及最後新情境答案選取新 skill，接受 `I wish I had gone to bed earlier.`，明確完成，區分已教結構的有支援運用和自行組織的表達。 |
| 最終來源、翻譯回歸 | 普通翻譯要求自動讀取 translator，回覆 Spoken／Direct Message／Writing 三版，保留不確定性與不要等的意思，未誤開練習。 |
| 最終來源、第二組連續流程 | 指定 AI 中文及「昨天太晚睡」新情境，第一輪只給中文等待；第二輪接受正確回譯、比較 wish + had + 過去分詞的來源效果，再給指定新情境並等待。 |

前兩案為同一 thread 的兩個真實模型回合。第三輪回覆等待超過 180 秒，已終止並記為未完成，沒有將該輪或原定後續案例計入通過。最後的收尾措辭修訂後，重新安裝到同一暫存設定，確認新 skill 安裝檔與最終 repo 來源逐 byte 相符，再以新工作階段執行自動回譯、合成收尾、翻譯回歸三案；它們皆 completed。其中收尾測試使用提供的合成上下文，並非宣稱完整連續對話已在客戶端跑完。

為補齊完整循環，以最終來源另跑第二組三輪連續情境。前兩輪 completed，新情境作答 `I wish I had gone to bed earlier.` 送出後，等待第三輪完成事件超過 80 秒，已終止且未計為通過。這與合成上下文收尾已通過的結果分開記錄，不宣稱已查明逾時原因。

獨立行為檢查補足各階段的觀察，但不替代尚未完成的客戶端完整多回合循環；目前有載入、七個成功模型回合、兩組各兩輪連續作答的證據。測試結束已移除暫存認證連結，保留原認證不動。

公開協定依據：[OpenAI 官方 app-server 文件](https://learn.chatgpt.com/docs/app-server)；實際觀察以本輪客戶端回覆為準。

## 交付界線

遷移回合完成 repo 來源與封裝；後續使用者要求升級目前 plugin，已更新私人帳號至 `0.1.2` 並完整讀回比對，見[套用紀錄](personal-deployment.md)。個人 CLI 固定來源與原來源專案維持原狀。未發布 tag／GitHub Release。Codex TUI／桌面 selector、ChatGPT 帳號新版的使用者可見行為及 Claude Code 新入口均未實測；既有版本的通過紀錄不套用到新入口。少量合成案例不代表所有語言現象或自動匹配都可靠。
