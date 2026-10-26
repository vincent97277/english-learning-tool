# 固定版本安裝、更新與交付驗收

日期：2026-10-26。Codex CLI 0.162.1；模型 smoke 回報 `gpt-6.1-sol`。僅使用暫存設定根、空工作目錄及合成文字。未修改個人 plugin、登入設定或公開 tag，沒有發布 Release。

## 邊界與 red → green

沿用 host 載入 → discovery → 選 skill → 可見輸出的既定邊界，不增加測試框架。Red：新隔離設定的 `plugin list --json` 回傳 `installed=[]`、`available=[]`，使用者尚無本 plugin 可選。Green：從固定 GitHub commit 安裝後出現版本 `0.1.0`，`skills/list` 同時回傳兩個整合 skill，無 discovery errors，實際輸出符合下表。

## 真 GitHub 固定來源

來源：公開 repo `vincent97277/english-learning-tool`，完整 commit `4943067c098dab199c1e7ce96e60f79b39d886f6`。這是整合分支已推送的開發 commit，包含完整雙 skill；不是發布 tag，也不是包含本份新文件的 commit。

在已建立的隔離 `CODEX_HOME` 中執行：

```sh
codex plugin marketplace add vincent97277/english-learning-tool --ref 4943067c098dab199c1e7ce96e60f79b39d886f6 --json
codex plugin add english-learning-tool@english-learning-tool --json
codex plugin marketplace list --json
codex plugin marketplace upgrade english-learning-tool --json
codex plugin add english-learning-tool@english-learning-tool --json
```

結果：add／upgrade／安裝皆成功，`upgrade errors=[]`；refresh 後 marketplace snapshot 的 `git rev-parse HEAD` 仍為選定 commit，安裝版本仍為 `0.1.0`。兩 catalog 均以 local root `./` 指向同 checkout 的 plugin，沒有另抓 main 的 Git plugin source。來源、snapshot 與安裝快取的兩份 skill SHA256 各自一致：

| Skill | 固定來源、snapshot、安裝後相同 SHA256 |
| --- | --- |
| english-translator | `9e4f5b4ee6faaf6a42d20c637c883491340901b3aea6dad79614b0eaa0bac4e5` |
| english-patterns | `67391ec97f829223670c9ab7835860d737022b1c94fa0d4d8707dba2141beb6c` |

只有「GitHub 固定 commit 的安裝與 refresh」用真網路來源；公開 main 隨後變動的完整 lifecycle 用下列本地產品 fixture 驗證，不能將兩者混稱網路發版驗收。

## 產品內容的兩版 Git fixture

從上述產品 commit 匯出完整 repo 作 disposable 本地 Git origin。第一版完整保留產品內容與版本 `0.1.0`；第二版僅將兩 manifest 的版本改為 `0.1.1`，並在兩個 skill 尾端附無功能的 fixture 註解，讓安裝 hash 可區分。這些測試版本與 tag 只在本地 fixture，從未推送。

Git CLI 不接受 `file://` marketplace source；測試使用 `https://fixture.invalid/english-learning-tool.git`，只在各 subprocess 的 Git environment 以 `url.<local-origin>.insteadOf` 精確改寫至本地 fixture。沒有連到 `.invalid`、修改 global Git config 或建立網路服務。這是測試運輸替身，不是產品安裝來源；實際 host 的 Git marketplace／cache 路徑照常運作。

| 操作 | 觀察 |
| --- | --- |
| origin 只有 `fixture-old`，固定此 tag 安裝 | snapshot `a496d032bb307e65da41569caf596269c288b45e`，enabled plugin 版本 `0.1.0`，兩 skill hash 如上表。 |
| origin main 增加新 commit 與 `fixture-new`；仍保留 old pin，執行 marketplace upgrade 與 plugin add | snapshot、版本與兩 hash 全不變。 |
| 同名 marketplace 直接 re-add，但 ref 改為 `fixture-new` | CLI exit 1，明確回報 already added from a different source、須先 remove；不假裝原地切版成功。 |
| 只在本次可丟棄隔離設定 remove → add new ref → plugin add | snapshot `4f81fe07d1c34d3fc7f977d5e4b1eb49f18d49b4`，enabled plugin 版本 `0.1.1`。 |
| 明確切版後的已安裝內容 | Translator SHA256 `c7c704d5b5dd14939e51820d51593ed64e5346fd2bb991e51769c9a2f7804be6`；Patterns `f92221c7fff665cd07f71c0fb9b40314f168ef26d20bcfebcc119e7e816a1515`，均與選定新 snapshot 一致。 |

重現時先從產品內容建立自己的兩個本地 synthetic commits／annotated tags，再使用隔離 profile 依序執行 `marketplace add <source> --ref <old>`、plugin add；新增新版後 upgrade／add，檢查 pin／版本／hash；確認直接 re-add 被拒，再僅在可丟棄 profile remove／以 new ref add／安裝。每階段比較 active plugin 與 snapshot，不能只看到磁碟殘留目錄就判成功。tag 未移動；同名 tag 被重寫的行為不在此測試承諾內。

移除 marketplace 會影響來源的全部安裝；既有 Claude fixture 探索另明示會清除其可管理的 options／secrets／data。產品文件因此優先建議新隔離 profile 驗新版，再由使用者決定遷移，不提供無聲移除個人來源的流程。

## 新來源與更新後最小模型回歸

從空暫存 cwd 啟動 Codex app-server，經 `skills/list` 取得已安裝 skill 的名稱與路徑；明確案例送公開 `skill` input，自動案例只送普通文字。沒有把 skill 本文貼進 prompt。每案新 ephemeral thread，read-only sandbox；未操作 CLI TUI selector。

| 來源與操作 | 合成輸入 | 可見結果 |
| --- | --- | --- |
| GitHub 固定 commit，明確選 Translator | 我可能會晚 10 分鐘，但還沒確定；請不要等我。 | Spoken、Direct Message、Writing 三版，保留 10 分鐘、否定及不確定性；沒有句型課。 |
| 同 commit，明確選 Patterns | 簡短解釋 `I look forward to hearing from you.`，只給兩個附中文例句 | 繁中說明介系詞 to 與 V-ing，恰兩個中英例句，不恢復完整密度。 |
| 明確切至 fixture-new 後，自動混合要求 | 翻成英文並解釋句型，只要一版，講解簡短、不用例句：我可能得晚點才能回覆。 | 一版 `I might not be able to reply until later.`，搭配簡短繁中句型說明，沒有強加三版或例句。 |

之前九個翻譯與十五個句型／切換／並存案例見[翻譯紀錄](translation.md)與[句型紀錄](patterns-and-switching.md)，本輪只跑與新來源／更新相關的三個最小回歸。模型用的兩個暫存認證連結已移除，原始認證保留；原始 auth、logs 或私人路徑沒有提交。

## 其他平台與發版準備

- **Claude Code**：使用者沒有 Claude Code，明確允許先不測。本輪不新增執行，沿用此前 2.1.310 的本機 validate／安裝／inventory 證據。產品 GitHub 固定 ref、refresh、明確切版與語言輸出均未通過驗收，不以先前 synthetic fixture 取代產品證據。
- **Codex 桌面**：工具禁止操作此 app，沒有繞過限制；安裝、選取、模型行為、並存與更新均待補。
- **版本與文件**：根 manifest 與 Claude manifest 維持 `0.1.0`、識別／描述／MIT 一致；catalog 無額外版本，來源同 checkout。CHANGELOG、維護流程與 Release 草稿已備妥。沒有公開 tag，正式 tag 安裝驗收需發布時再做。
- **公開內容**：檢查 manifest parser、文件連結、diff 與私人資料排除；這些只輔助封裝／交付，不能代替平台行為。

工單保留跨客戶端驗收未完成，依使用者授權先交付實作與發版準備，不宣稱已完整支援三客戶端。
