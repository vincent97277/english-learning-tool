# alpha 與 GitHub 並存的誤用檢查

這是 2026-10-26 修正前的歷史紀錄。後續命名修正、429 診斷與部署結果見[2026-10-27 驗收](source-isolation-2026-10-27.md)。

日期：2026-10-26。範圍：帳號版 `English Learning Tool-alpha`／0.1.3 與 GitHub 版 `English Learning Tool`／0.1.0 同時提供 skills；只驗證，不修改正式安裝、名稱、啟用設定或帳號 release。

## 結論

只有 plugin 顯示名稱加上 `-alpha`，不足以唯一區分 skill 指令。兩份 translator／patterns 的完整名稱仍相同；來源要靠 plugin ID 與檔案路徑區分。已測案例未觀察到錯誤翻譯輸出，但不能據此宣稱沒有選錯來源的風險。

## 方法與限制

- 複製實際安裝快取的帳號版 0.1.3 與 GitHub 版 0.1.0，逐 byte 確認三份／兩份 skill 與原安裝相同。保留原 manifest 與 skill 名稱、描述及內容。
- 在暫存 Codex 設定根建立兩個 local marketplace：`probe-account-alpha` 與 `probe-github`，同時安裝；空工作目錄、ephemeral thread、read-only、approval never。使用既有登入的暫存連結，結束移除連結。
- 透過 app-server 的 `skills/list` discovery 取得實際名稱與路徑。明確案例傳入 `skill` input 的 name／path；文字案例不傳選取項。未修改 skill 加入標記，也未在 prompt 貼上完整 skill 正文。
- 這是兩份真實內容的隔離並存測試，不是實際帳號 remote adapter、原生桌面 `@` UI 或使用者點選操作的端到端證據。fixture 的路徑含有 alpha／github 提示，因此文字指定來源成功的結果不能外推為實際環境穩定保證。

## 可重現的名稱碰撞

Discovery 同時回傳五個 enabled 入口：

| 完整 skill 名稱 | 帳號版 | GitHub 版 |
| --- | --- | --- |
| `english-learning-tool:english-translator` | 1 | 1 |
| `english-learning-tool:english-patterns` | 1 | 1 |
| `english-learning-tool:english-back-translation` | 1 | 0 |

同名的兩項有不同 `pluginId` 與 `path`，但 `name` 本身沒有 alpha 後綴。這次 discovery 項目只有 name、description、path、pluginId、scope、enabled，沒有 plugin 顯示名稱欄位；桌面 UI 是否額外查父 plugin 的名稱，未直接驗證。

## 模型案例

| 情境 | 觀察 |
| --- | --- |
| 明確選帳號 translator 的 name／path | 回覆一版 `I might be ten minutes late.`，符合請求。來源由送入的選取項指定；未另外觀察到讀檔命令，不以輸出相同反推來源。 |
| 明確選 GitHub translator 的 name／path | 同樣回覆一版自然英文，沒有多出句型課。來源由選取項指定。 |
| 純文字指定 English Learning Tool-alpha | 此 fixture 中觀察到讀取帳號 translator，回覆一版，保留未決定與不要等的意思。 |
| 只寫 `$english-learning-tool:english-translator` | 輸出一版正確翻譯，但未觀察到可確認來源的讀檔命令。完整名稱仍碰撞，不能把這案列為來源辨識通過。 |
| 明確選帳號回譯入口 | 給繁中題目並等待，未提前給英文答案。 |

以上五個回合均 completed。回譯接續同一 thread 的 `I wish I leave earlier.` 作答，等待完成事件超過 90 秒，已終止；未算作通過，也未推定為 skill 誤用或已查明逾時原因。

另以新的單回合工作階段提供完整的合成練習上下文，嘗試確認接續回饋而非翻譯；同樣等待超過 90 秒而未完成。原定管理詢問負例未執行。這兩項不列為通過，不再以連續重試增加模型呼叫；它們不影響名稱碰撞已由 discovery 重現的結論。

成功案例與私有 inventory 保留在 gitignored 的 `.acceptance-local/alpha-source-selection/`。測試已移除暫存認證連結，沒有修改正式帳號或 GitHub 安裝。

## 封裝與比對保護

以 repo 根目錄比對目前 alpha 帳號版，會非零失敗，固定輸出指出 `extensions` 與 `version` 不同；沒有放寬或忽略差異。改以這次獨立 alpha 封裝副本為 `--root`，比對通過，inventory matches 為 true、component mismatches 為 0。

這證明現行檢查能攔下把 alpha release 當作無後綴 repo 來源的錯誤比對，但不是來源唯一選取機制。

## 後續方向

GitHub 版維持原樣。若要讓 `@` 名稱及純文字完整 skill 指令都可唯一區分，帳號版各 skill 的識別名稱也需要獨立，例如 `english-translator-alpha`／`english-patterns-alpha`，並同步目錄及引用。這是後續命名變更建議，本輪沒有實作或發布。
