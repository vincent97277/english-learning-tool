# 個人環境與 ChatGPT 私人帳號套用

日期：2026-10-26。使用者授權將完成的新版套用 Codex／ChatGPT，測試通過後下架舊插件。本次將「下架」執行為解除安裝舊版，保留其帳號原始插件供回復，沒有永久刪除或公開目錄發布。

## 安裝內容

- Codex CLI 0.162.1 的個人環境，以固定 GitHub commit `4943067c098dab199c1e7ce96e60f79b39d886f6` 登記並安裝 `english-learning-tool@english-learning-tool`，版本 0.1.0，enabled=true。
- ChatGPT 以 Plugin Creator 儲存新的 USER／PRIVATE 插件 English Learning Tool 0.1.0。封裝只包含根 manifest、LICENSE 與兩份 skill，不包含 repo marketplace、私人設定或驗收輸出。帳號管理頁顯示「解除安裝」，兩個 skill 的使用開關均為 on，確認已安裝。
- 根 manifest 在既有 schema 上增加 OpenAI 顯示資訊，保留名稱、版本、描述、授權與原 author。最終來源、重建的 ZIP 與帳號讀回 manifest 均通過拒絕重複鍵的 JSON 檢查。服務將帳號版的作者與 developerName 正規化為帳號資料；除這兩項預期差異外，manifest 解析結果一致，未將帳號資料複製至公開 repo。
- 帳號讀回及 Codex 安裝後的兩份 skill 均與 repo 完全相同，SHA256 沿用[固定來源驗收](fixed-version-delivery.md)的兩個值。沒有改寫語言行為。

## 核心行為

Codex 從空工作目錄啟動 app-server，使用個人登入及設定；工作階段為 ephemeral、read-only，拒絕任何額外 approval。`skills/list` 兩個新版 skill 均為 enabled，discovery errors=[]；明確案例使用 host 回傳的 skill 路徑，未將本文貼進 prompt。ChatGPT 網頁先明確選取 English Learning Tool，於同一個測試對話依序執行三案。

| 合成案例 | Codex | ChatGPT 網頁 |
| --- | --- | --- |
| 翻譯「我可能會晚 10 分鐘，但還沒確定；請不要等我。」 | Spoken、Direct Message、Writing 三版，保留時間、否定與不確定性。 | 同樣提供三版，保留原意。 |
| 簡短解釋 `I look forward to hearing from you.`，只給兩個附中文意思例句 | 繁中說明 `to` 為介系詞、後接 V-ing，恰兩個中英例句。 | 同樣說明結構與介系詞，恰兩個中英例句。 |
| 翻譯並解釋「我可能得晚點才能回覆」，單版、簡短、不用例句 | 一版 `I might not be able to reply until later.` 與簡短繁中說明，無例句。 | 一版相同英文與繁中說明，無例句。 |

以上六個案例按使用者可見輸出檢查通過。沒有重跑前期完整觸發矩陣，也沒有把同一對話的續問視為獨立新對話測試。

## 舊版移除

核心測試通過後，使用官方 Plugin Management 一次解除安裝 English Patterns 0.8.0 與 English Translator 0.13.0，兩項均回報 uninstalled。ChatGPT 已安裝清單最初顯示舊快取；重新載入後確認兩項消失，English Learning Tool 仍在。保留兩個原始私人插件，沒有執行「刪除外掛程式」。

## 證據與界線

私人驗收輸出保存在 gitignored 的 `.acceptance-local/personal-install/`，包含帳號讀回、個人環境 discovery、三案完成狀態及可見輸出、插件 inventory 和替換後畫面。公開 repo 不提交該資料夾。

ChatGPT 網頁已實測，Codex CLI 個人環境已實測。工具明確禁止控制 ChatGPT／Codex 原生 app，因此 **Codex 桌面 selector、ChatGPT 桌面 Chat、手機與桌面完整更新 lifecycle 未測**。網頁瀏覽器連線中斷並恢復後，改用可操作的 Edge 原生介面完成網頁測試；沒有控制被禁止的原生 app。CLI／網頁證據不替代原生桌面驗收。

未發布公開 tag、GitHub Release 或公開 Plugins Directory 項目；私人帳號儲存不等於公開發版。

## 0.1.1 工具集合描述與維護改善

同日依使用者授權完成：

- 根與 Claude manifest 升為 0.1.1，description 統一描述為英語學習工具集合；帳號版 shortDescription 為「英語學習工具集」，longDescription 說明目前工具成員與搭配使用方式。
- README 將最短指令與一次設定後只貼內容的用法放在安裝步驟之前。
- 新增 `scripts/plugin.py` 的來源檢查、實際 ZIP 檢查／封裝與只輸出固定欄位差異的帳號比對；11 項針對重複鍵、metadata 漂移、YAML、過期封裝與輸出遮蔽的測試通過。
- 新增 GitHub Actions 工作執行相同靜態檢查與封裝，未執行模型測試或自動發布；遠端工作尚未觸發。
- 以原私人 plugin ID 與觀察到的 release ID 更新為 0.1.1，保留 USER／PRIVATE 與既有身分；重新列出全部檔案並讀回比較通過。讀回的作者欄位先遮蔽，再保存於私人驗收目錄，工具輸出僅包含固定欄位路徑與計數。

Codex CLI 的固定 GitHub 來源保持原 0.1.0 commit；本次私人帳號 metadata 更新與 GitHub 固定來源切版分開紀錄。兩份 skill 與先前六案驗證內容逐位元相同，因此未重跑模型案例。原生桌面驗收缺口保持不變。

## 0.1.2 回譯工具升級

2026-10-26，使用者在回譯遷移完成後要求「升級目前的 plugin」。依現有私人 plugin 身分更新，保留 USER／PRIVATE、原 plugin ID 與權限，沒有另建 plugin。

- 升級前完整列出並讀取 0.1.1 的 5 個檔案；除允許的帳號 metadata 欄位外，manifest、LICENSE 與既有兩份 skill 均符合遷移前來源，沒有不明資產或設定需要搬移。
- 重新檢查最終 0.1.2 ZIP 與 repo 相符，使用剛讀到的 release ID 作為 expected release，避免覆蓋並行更新；更新回報成功，版本 0.1.2。
- 升級後完整列出並讀回 6 個檔案：根 manifest、產生的 compatibility manifest、LICENSE 與三份 skill。讀回 release 與更新回傳一致。
- `compare-account` 通過：manifest differences 為空、inventory matches 為 true、component mismatches 為 0；本次沒有需要容許的 author／developerName 正規化差異。
- 私人讀回資料保存在 gitignored 的 `.acceptance-local/back-translation-upgrade/`，公開文件不收錄作者資料、原始工具回覆或學習內容。

這次確認帳號 release 已儲存且內容一致；目前 chat 已載入的舊內容不當作新版 runtime 證據。新入口的隔離 Codex 行為及連續第三輪逾時見[回譯驗證](back-translation.md)，尚未補做帳號新版網頁／桌面行為。Codex 個人 CLI 的固定 GitHub 來源仍為 0.1.0，未切換來源；未建立公開 tag 或 GitHub Release。

## 帳號版 0.1.3：顯示名稱加上 -alpha

2026-10-26，使用者要求 GitHub 版保留原樣，帳號版以後名稱加上 `-alpha`。這次更新既有私人 plugin 的顯示名稱為 `English Learning Tool-alpha`，保留原 package name、plugin ID、USER／PRIVATE 及全部 skill 識別名稱。

- 更新前完整讀回 0.1.2 的 6 個檔案，與 repo 比對通過。
- 從 repo 派生 gitignored 的 `.acceptance-local/account-alpha/source/` 封裝副本，只調整根 manifest 的顯示名稱及副本的根／Claude manifest 版本為 0.1.3。檢查只有這兩項語意變更，三份 skill 與 repo 完全一致。
- 來源及實際 ZIP 檢查通過後，使用當前 release ID 防止覆蓋並行更新；帳號更新成功。
- 更新後完整讀回 6 個檔案，確認 release 一致、顯示名稱符合 `-alpha` 後綴；以 alpha 副本為 `--root` 執行 `compare-account`，manifest differences 為空、inventory matches 為 true、component mismatches 為 0。
- GitHub repo manifest 仍為 0.1.2／English Learning Tool；既有 GitHub 安裝仍為 0.1.0，固定 commit 未切換。沒有更名、停用或移除 GitHub 版。

這次只改帳號顯示資訊與版號，未重跑語言行為。尚未直接驗證外掛頁及 `@` 選單呈現；兩個來源的 skill 名稱保持相同，更名不代表重複入口被合併。之後帳號更新依[alpha 封裝流程](../maintaining.md#帳號版的-alpha-命名與封裝)保留後綴，讀回以該次封裝副本為準。

## 2026-10-27：GitHub 固定安裝升至 0.1.2

- 更新前以 CLI 確認 `english-learning-tool` marketplace 僅有此一 plugin，版本 0.1.0、enabled；僅保存該來源及該 plugin 的設定，不備份認證或其他設定。
- 官方 CLI 移除該 marketplace、重新登記已推送的固定 commit `8e9abb226c17a26c6c3cb535871e53a8f2ceb7eb`，再安裝同一 plugin。結果為 0.1.2、enabled=true；沒有更動帳號版或其他 marketplace。
- 來源快照及原生 discovery 回傳的安裝快取，根 manifest、LICENSE 與三個 skill 共五個檔案均逐位元符合該 commit；三個入口 enabled。
- `plugin/list` 明確要求 local 及 created-by-me-remote catalog 並重新取得，然後 `skills/list` 強制重掃，確認帳號仍為 0.1.3；更新前有兩組完整名稱碰撞，GitHub 新增回譯入口後為三組。不能以顯示名稱後綴視為來源已唯一。
- 帳號 0.1.4 候選已準備。自動核准審查拒絕包含刪除三個舊 SKILL.md 路徑的更新，未接受先前的名稱修正授權；已請使用者明確確認帳號更新及路徑替換，尚未部署，也未以其他 plugin 或殘留舊入口繞過。

本輪行為結果及 review 見[來源隔離驗收](source-isolation-2026-10-27.md)。原生桌面 `@` 選單仍未手動操作；未建立公開 tag 或 GitHub Release。
