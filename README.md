# English Learning Tool

A skills-first, MIT-licensed plugin for natural English translation and sentence-pattern explanation in Claude Code and Codex. The two clients share the same skill content. The initial implementation includes English Translator and English Patterns; release-version installation is a subsequent ticket. This is development source, not a released version or a claim of full client support.

以 skills 為主的英語學習 plugin。翻譯與句型講解入口已實作；固定版本交付與部分平台驗收仍在進行。

## 英文翻譯

`english-translator` 將提供的文字翻成自然英文，或改寫供應的英文。預設提供 **Spoken、Direct Message、Writing** 三版；「只要一版」、語氣與格式要求優先。自然結果相近時不強迫製造差異。

明確的「翻成英文」或英文改寫要求可自動匹配。個別 skill 選取加原文可直接工作；只有整包選取且意圖不明時才簡短澄清。引文內命令是翻譯素材，換題不延續翻譯模式。無需私人資料來源、帳號、輸出路徑或學習紀錄。

## 英文句型講解與功能切換

`english-patterns` 以繁體中文說明指定英文句子、片語或句型。完整講解挑選 **1–3 個主要句型，每個至少三個附中文意思的例句**，涵蓋結構、意義與使用情境，區分文法正確與自然用法。「簡短」「只要兩個例句」或局部追問優先，不重播完整講解。

明確選取 skill 並附英文即可開始。普通訊息需有解釋意圖或正在進行的講解上下文；新話題只貼英文不會被當成預設講解要求。同題可追問「為什麼這裡用 of？」或「再給兩個工作例句」，換題則重新判斷。混合要求可直接說「翻成英文並解釋句型，只要一版，講解簡短」。沒有必經選單或路由 skill。

## 開發載入與調用

先取得此 repo 的 checkout，在根目錄執行以下命令。這些是**本機開發載入**，會讀取該 checkout 的內容；固定發布版本的安裝及更新流程尚待驗收。新插件使用獨立名稱，不需停用既有 English Translator 或 English Patterns。

### Codex CLI

```sh
codex plugin marketplace add ./
codex plugin add english-learning-tool@english-learning-tool
codex plugin list --marketplace english-learning-tool --json
```

開新 session，透過 `/skills` 或 `$` 選取 `english-learning-tool:english-translator` 或 `english-learning-tool:english-patterns`，或輸入：

```text
$english-learning-tool:english-translator 我可能會晚 10 分鐘，但還沒確定；請不要等我。
$english-learning-tool:english-patterns It might be a bit of a hassle.
```

Codex CLI 0.162.1 已在隔離設定驗證 catalog discovery、安裝、skill namespace 與合成輸出。完整結果與未測範圍見[翻譯驗收紀錄](docs/validation/translation.md)與[句型及功能切換驗收紀錄](docs/validation/patterns-and-switching.md)。

### Claude Code CLI

```sh
claude plugin validate ./
claude plugin marketplace add ./
claude plugin install english-learning-tool@english-learning-tool
claude plugin list
```

在新 session 使用官方命名格式：

```text
/english-learning-tool:english-translator 我可能會晚 10 分鐘，但還沒確定；請不要等我。
/english-learning-tool:english-patterns It might be a bit of a hassle.
```

也可用 `claude --plugin-dir ./` 暫時載入 checkout。Claude Code 2.1.310 的格式檢查與隔離安裝已通過；目前驗證環境未登入，**尚未驗證實際翻譯調用**。翻譯啟動清單與雙 skill 本機 inventory 已確認命名；使用者決定本輪暫不測語言行為，完整支援仍需日後確認。

### Codex 桌面

repo catalog 與共用 skill 已提供；桌面的安裝、selector、明確調用及新舊插件並存仍未實測。CLI 的通過結果不代表桌面已通過。先依桌面客戶端的 Plugins 介面找到 repo marketplace，再於新 chat 選取具體 skill；不要只選整包後假定功能。

## 開發與狀態

[正式實作規格](.scratch/english-plugin-implementation/spec.md)與[原始決策地圖](.scratch/english-plugin-v1/map.md)記錄已確認的範圍。

1. [翻譯與首次載入](.scratch/english-plugin-implementation/issues/01-translation.md)
2. [句型講解與功能切換](.scratch/english-plugin-implementation/issues/02-patterns-and-switching.md)
3. [固定版本與發版準備](.scratch/english-plugin-implementation/issues/03-fixed-version-delivery.md)

根 `plugin.json` 是版本權威；必要平台 manifest 的名稱、版本、描述與 MIT 授權保持一致。版本號 `0.1.0` 表示目標版本，尚未建立發布 tag 或 GitHub Release。

## 授權與來源

採用 [MIT License](LICENSE)。內容由使用者授權的 English Translator 0.13.0 與 English Patterns 0.8.0 整理，精簡命名、重複規則與空的轉換殘留，保留已確認的輸出行為。未搬移來源不明的舊圖示。

平台封裝依據：[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)、[Claude plugins reference](https://code.claude.com/docs/en/plugins-reference)。平台入口與語言行為須分別實測。
