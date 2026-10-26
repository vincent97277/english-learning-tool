# 維護與版本流程

本專案以少量 Markdown skills 與平台 metadata 為主，使用一支 Python 檢查／封裝工具與輕量 CI；不需要常設 develop 分支、建置系統或自動發版。

## 檢查與封裝

首次準備開發環境：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

變更後執行：

```sh
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/plugin.py check
.venv/bin/python scripts/plugin.py pack --output /tmp/english-learning-tool.zip
```

`pack` 先檢查來源，再只收進根 manifest、LICENSE 與 skills，並讀回實際 ZIP，確認檔案清單與每份內容均符合來源。輸出路徑須在 repo 外且尚不存在；封裝後若修改來源，重新封裝至新檔案。手動檢查既有 ZIP 可用 `check --archive <path>`。CI 對 push／pull request 執行相同的測試、來源檢查與實際 ZIP 檢查，不呼叫模型或發布插件。

檢查涵蓋 JSON 重複鍵、必要 manifest 欄位、共用 metadata 一致性、catalog 指向、YAML frontmatter、skill 入口與封裝內容。它是本專案的靜態檢查，不宣稱取代完整外部 schema 驗證或平台行為驗收。

## 工具探索與帳號比對

探索工具先以 `ALL_TOOLS` 的 `name` 篩選相關命名空間，只輸出名稱清單；選定工具後才讀取該工具的完整規格。已知 plugin ID 時直接讀取該插件，避免重做全目錄搜尋。帳號、來源與安裝快取分別核對；修改 repo 或帳號來源，再經支援的安裝／更新流程套用。

帳號工具讀回的完整結果保留在工作中的私有變數，顯示時只投影操作成功與否、版本、scope、檔案數及分頁狀態。需要本機比對時，輸入放在 gitignored 的 `.acceptance-local/`；不要直接印出原始結果、作者欄位、檔案正文或解析器例外。

```sh
.venv/bin/python scripts/plugin.py compare-account --readback .acceptance-local/account-readback.json
```

輸入是 `get_plugin_files` 的資料物件，須取得完整 inventory，並讀取 manifest、產生的 compatibility manifest（若有）、LICENSE 與全部 packaged skill 檔案。先完成每頁清單，將最後的 `next_offset` 設為 null。指令只輸出固定欄位路徑、數量與是否相符，失敗以非零狀態結束；原始值不會印出。僅容許服務正規化 `author.name`、`author.email` 與 `extensions.com.openai.interface.developerName`，其他 manifest 差異或缺檔均視為失敗。

更新私人帳號插件前，依 Plugin Creator 的更新流程保存目前 release ID，先檢查 ZIP，再以該 ID 防止覆蓋並行更新；更新後重新讀回比對。帳號 metadata 正規化不覆寫公開 repo 的作者資訊。

### 帳號版的 alpha 命名與封裝

2026-10-26 起依使用者要求，兩個分發來源採以下規則：

- GitHub 版保留 `English Learning Tool`，repo manifest、package name、marketplace 及既有固定 ref 安裝不因帳號更名而修改。
- 帳號版的 `extensions.com.openai.interface.displayName` 固定為 `English Learning Tool-alpha`。更新既有私人 plugin，不另建身分；package `name` 保持不變。2026-10-27 使用者進一步確認：三個帳號 skill 的識別名及目錄也加上 `-alpha`，GitHub skill 名稱維持原樣。
- 帳號版每次有修改仍須升版。本次顯示名稱修訂為帳號版 `0.1.3`；repo 來源維持 `0.1.2`，既有 GitHub 安裝維持 `0.1.0`。`-alpha` 是顯示名稱後綴，不是 SemVer prerelease 欄位。

帳號更新以 `account-source` 從當次 repo 來源派生獨立副本，放在 gitignored 的 `.acceptance-local/`，而非修改 GitHub manifest。副本只包含根 manifest、LICENSE、skills、檢查所需的兩份 Claude metadata 與 Codex catalog；不複製認證、快取或學習資料。命令保留 manifest 其他設定及技能正文，修改顯示名稱、skill 名稱／目錄與副本的根／Claude manifest 版號。它拒絕覆寫既有目錄，也拒絕把已派生的 alpha 副本再次當作 GitHub 來源，避免產生 `-alpha-alpha`。

目標版本須高於目前帳號 release，且不低於使用的 repo 來源版本；操作者先讀帳號現有版本再指定，更新工具仍以 observed release ID 與服務端版本檢查防止覆蓋或降版。版本格式檢查不等於已檢查遠端的版本順序。

先核對帳號現有 release 與先前封裝副本，處理任何非預期差異，再準備新版副本。共用 skill 正文直接取自本次 repo；若帳號有另外保留的設定，須逐項保留或確認差異用途。以下是 0.1.4 的命令範例：

```sh
.venv/bin/python scripts/plugin.py account-source --version 0.1.4 --output .acceptance-local/account-alpha-0.1.4/source
.venv/bin/python scripts/plugin.py --root .acceptance-local/account-alpha-0.1.4/source pack --output /tmp/english-learning-tool-alpha-0.1.4.zip
.venv/bin/python scripts/plugin.py --root .acceptance-local/account-alpha-0.1.4/source compare-account --readback .acceptance-local/account-alpha-0.1.4/after.json
```

每次使用新的副本與尚不存在的 ZIP 路徑，依當次版本調整例中的名稱。檢查實際 ZIP 後，以讀到的 release ID 作 guarded update；更新後完整讀回，確認名稱、版號、既有身分及全部檔案。帳號比對的 `--root` 必須指向該次 alpha 副本，不能直接與無後綴的 repo manifest 比較，也不增加忽略名稱／版本差異的寬鬆規則。

從舊帳號版遷移時，要用 inventory 裡的精確路徑移除被新 alpha skill 取代的三份舊 SKILL.md；不能只新增 alpha 檔案而保留舊入口。先確認已獲得帳號更新及路徑替換授權，再更新；完整讀回必須確認舊路徑消失。若更新被拒絕，不另建 plugin 或保留舊入口作為繞過方法。

只改顯示名稱不足以消除碰撞，見[修正前檢查](validation/alpha-source-selection.md)；2026-10-27 的命名修正、實測及部署狀態見[來源隔離驗收](validation/source-isolation-2026-10-27.md)。兩個來源的安裝各自保留；沒有來源要求的自然語言任務仍可能選任一適用來源，唯一名稱不等於所有意圖辨識皆正確。

## 日常修改

初版到 `0.1.0` 可在 main 開發；本次依 implement-spec 使用單一整合分支與各工單短命分支。首次發布後，重要行為、安裝、識別或版本變更從 main 開短命 `feat/…` 或 `fix/…`，只做相關修改，確認受影響的外部行為後提交簡短 PR。單人也可自我 review；純錯字可直接 main。預設只維護最新版，真有舊版修補需求再建立維護分支。

PR 說清楚使用者原問題、結果、驗證與限制。先讀實作規格及對應工單，對照 staged diff，排除私人設定、憑證、快取、真實學習資料及私人絕對路徑。研究分支保持歷史參考，不因實作而合併。

## 版本與發布

根 portable manifest 是版本權威；修改時同步 Claude manifest 的名稱、版本、描述與授權。catalog 沒有重複版本欄位；若日後增加，也必須一致。兩個 catalog 始終指向同一 checkout，避免 catalog 固定、plugin 卻另抓浮動 main。

上述規則套用於各自的來源：repo 根 manifest 管理 GitHub 來源版本；帳號 alpha 封裝副本的根 manifest 管理該次帳號 release。帳號副本不覆寫 repo manifest，兩者不用為了顯示名稱修訂強迫同版。

初期版本約定：修復升 patch，新能力或可觀察承諾調整升 minor。準備 `0.1.0` 不代表已發布。正式發布前完成 review、可用客戶端驗證、更新 CHANGELOG 與 Release 說明，逐項保留未驗證環境。尚未完成的驗收不能因改版本號而關閉。

只有取得發布授權後，才在選定且已推送的 commit 建立 annotated tag（例如 `git tag -a v0.1.0 -m 'English Learning Tool 0.1.0' <commit>`），推送這個 tag，再以同一 tag 建立簡短 GitHub Release。公開 tag 永不移動或覆蓋；錯版用新版本修正。不要以 main 或浮動 latest 作可重現安裝承諾。分支保護與 release immutability 本專案尚未啟用，也不是初版必要條件。

Release 只列實際通過的客戶端與已知缺口，不宣稱缺圖示的目錄上架檢查已通過。GitHub Release 與官方 plugin 目錄上架是不同操作，後者不在本次範圍。

## 驗證原則

優先走「客戶端載入 → 選取 skill → 使用者可見輸出」。JSON／frontmatter 格式與版本同步是輔助檢查，不能取代模型行為。重跑受影響情境；沒有新變更、失敗或未解風險時，不反覆跑整套合成案例。固定來源測試用隔離設定與合成 fixture，不移動公開 tag、不修改個人 plugin；清理自己建立的認證副本或連結，保留原始認證。
