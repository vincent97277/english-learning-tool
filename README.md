# English Learning Tool

以 skills 為主的英語學習 plugin，提供 **英文翻譯** 與 **英文句型講解**。Claude Code 與 Codex 共用同一份內容，採 MIT 授權；無需額外 MCP、後端、私人資料來源或學習紀錄。

目前為 `0.1.0` 發版準備，**尚未發布 tag 或 GitHub Release**。Codex CLI 已通過隔離安裝、固定來源與合成行為驗收；Claude Code 只有封裝／載入證據，使用者決定本輪暫不測語言行為；Codex 桌面仍待實測。詳見[驗證總覽](docs/verification.md)。

## 兩個獨立入口

| Skill | 用途與預設 |
| --- | --- |
| `english-translator` | 將提供的文字翻成自然英文，或潤飾提供的英文。預設 Spoken、Direct Message、Writing 三版；指定單版、語氣或格式時優先遵從。 |
| `english-patterns` | 以繁體中文解釋英文句子、片語或句型。完整講解挑 1–3 個主要句型，每個至少三個附中譯例句；簡短要求、例句數量與局部追問優先。 |

優先明確選取其中一個 skill，也可直接說「翻成英文」或「請解釋這個英文句型」。混合要求例如「翻成英文並解釋句型，只要一版，講解簡短」可一起完成。只選整包而用途不明時，會簡短澄清；沒有必經選單。裸英文不會自動變成句型課，換題重新判斷，引文內命令只當素材處理。

## 安裝與使用

先確認客戶端支援 plugin marketplace。下列命令使用已驗證、包含兩個 skill 的**固定開發 commit**；它不是已發布版本。正式版本發布後，改用 Release 對應的固定 annotated tag，避免以 `main` 安裝來期待版本不變。

若只想試用且保留原安裝，可在另一個設定目錄驗證；Codex 的 `CODEX_HOME` 必須先建立，獨立設定也需要自己的正常登入授權。不要複製認證到公開 repo。這個整合 plugin 使用不同識別名稱，不需停用舊 English Translator／English Patterns。

### Codex CLI

```sh
codex plugin marketplace add vincent97277/english-learning-tool --ref 4943067c098dab199c1e7ce96e60f79b39d886f6
codex plugin add english-learning-tool@english-learning-tool
codex plugin list --marketplace english-learning-tool --json
```

開新 session，透過 `/skills` 或 `$` 選取個別 skill，或使用以下明確名稱：

```text
$english-learning-tool:english-translator 我可能會晚 10 分鐘，但還沒確定；請不要等我。
$english-learning-tool:english-patterns It might be a bit of a hassle.
```

Codex CLI 0.162.1 已驗證 discovery、安裝與 app-server 的明確 skill 選取；文字入口已於翻譯案例驗證。CLI TUI 的 `/skills` 選單與桌面 selector 仍須分開確認。

### Claude Code CLI

以下是符合官方 CLI 格式的固定來源命令；**本專案的遠端固定來源 lifecycle 與模型輸出尚未實測**。

```sh
claude plugin marketplace add vincent97277/english-learning-tool#4943067c098dab199c1e7ce96e60f79b39d886f6
claude plugin install english-learning-tool@english-learning-tool
claude plugin list
```

在新 session 使用：

```text
/english-learning-tool:english-translator 我可能會晚 10 分鐘，但還沒確定；請不要等我。
/english-learning-tool:english-patterns It might be a bit of a hassle.
```

Claude Code 2.1.310 的格式檢查、隔離本機安裝與雙 skill inventory 已通過；實際調用與語言行為待日後有環境時驗收。

### Codex 桌面

repo catalog 與共用 skill 已提供。桌面安裝、兩個 skill 的 selector、調用、輸出及舊版並存仍未驗證，不以 CLI 結果代替。桌面測試需在支援 marketplace 的環境開新 chat，選取具體 skill 後使用上方合成文字確認結果。

## Refresh 與切換版本

保留原 ref 的 refresh 是重新讀取同一來源，**不會選擇新版 ref**。Codex CLI 0.162.1 已在固定 GitHub commit 與兩版產品 fixture 驗證：

```sh
codex plugin marketplace upgrade english-learning-tool
codex plugin add english-learning-tool@english-learning-tool
```

Claude 的對應入口為 `claude plugin marketplace update english-learning-tool`，再執行 `claude plugin update english-learning-tool@english-learning-tool`；產品的固定來源更新仍待實測。

要改成另一個 ref，兩個受測 CLI 均拒絕直接重複 add 同名但不同來源的 marketplace。先以新的隔離設定根試新版，再決定遷移現有安裝。若在原設定移除並重新登記來源，須先列出該來源所有 plugin 並保留所需設定：**移除 marketplace 會影響其全部安裝；Claude 明示也會清除它們可管理的 options、secrets 與 data。** 本 plugin 不自行儲存學習資料，但不能據此保證客戶端移除無影響。不要對包含其他 plugin 的來源照抄移除操作。

只對已確認可丟棄的測試設定，可依序使用 `marketplace remove english-learning-tool`、以上安裝命令改填新 ref、重新安裝，再開新 session 驗證。實際專案沒有自動移除任何個人來源。更新結果、限制與重現方式見[固定版本驗收](docs/validation/fixed-version-delivery.md)。

## 本機開發

在 repo 根目錄執行 `codex plugin marketplace add ./` 再安裝，可讀取當前 checkout；這是可變的開發來源。Claude 可用 `claude plugin validate ./` 檢查、`claude --plugin-dir ./` 暫時載入，或先 `claude plugin marketplace add ./` 再安裝。已登記同名來源時先另用隔離設定，不將開發 checkout 覆蓋固定安裝。

根 `plugin.json` 是版本權威。Claude manifest 的名稱、版本、描述、MIT 授權須一致，兩個 catalog 指向同 checkout 的 plugin 根目錄。沒有路由層、生成器或常設測試服務。

[實作規格](.scratch/english-plugin-implementation/spec.md)、[工單](.scratch/english-plugin-implementation/issues/03-fixed-version-delivery.md)與[原始決策地圖](.scratch/english-plugin-v1/map.md)保留決策與未完成驗收。維護與版本約定見[維護流程](docs/maintaining.md)，待發布內容見[CHANGELOG](CHANGELOG.md)與[0.1.0 Release 草稿](docs/release-0.1.0.md)。

## 授權與來源

採用 [MIT License](LICENSE)。內容由使用者授權的 English Translator 0.13.0 與 English Patterns 0.8.0 整理，改善命名、重複指令與空殼，保留已確認行為，未搬移來源不明圖示。

平台依據：[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)、[Codex developer commands](https://learn.chatgpt.com/docs/developer-commands)、[Claude plugin commands](https://code.claude.com/docs/en/plugins/cli-reference)。指令格式與文件支持不等於各客戶端已實測通過。
