# Changelog

## 帳號版 0.1.4 — skill 名稱區分，2026-10-27

- 依使用者明確授權，將三個帳號 skill 的識別名及目錄加上 `-alpha`，移除被取代的三份舊 SKILL.md；正文、plugin 身分及 USER／PRIVATE 範圍保留。
- 帳號六檔完整讀回、更新 release 核對及實際安裝快取比對均通過；重新取得正式來源並強制重掃 skills 後，六個入口 enabled、同名碰撞為零。
- GitHub 仍為 0.1.2 與固定 `8e9abb2`，沒有因帳號更新再升版。既有隔離模型結果適用於相同技能正文；本次驗證正式部署與載入，不重跑未變的語言案例。

詳見[來源隔離驗收](docs/validation/source-isolation-2026-10-27.md)。原生桌面選單未手動操作，不作所有自然語言要求皆不會誤選的保證。

## GitHub 0.1.2 更新 — 2026-10-27

- 推送既有回譯遷移與維護工具，將個人 GitHub 固定安裝從 0.1.0 更新至 `8e9abb2` 的 0.1.2；三個 canonical skill 名稱不變。
- 新增 `account-source`，從同一來源產生三份 `*-alpha` 入口；拒絕從 alpha 副本重複派生。當時帳號正式版為 0.1.3，0.1.4 路徑替換等待明確授權；後續已完成，見上節。
- 修正帳號 compatibility manifest 比對，拒絕不符的技能路徑及未知欄位；14 項測試、遠端 CI、封裝與實際安裝內容比對通過。
- 當時個人 discovery 確認兩來源有三組同名碰撞；後續正式零碰撞結果，詳見[來源隔離驗收](docs/validation/source-isolation-2026-10-27.md)。

沒有再次提高既有未交付的 GitHub 來源版本，也未建立公開 tag 或 GitHub Release。

## 帳號版 0.1.3 — alpha 命名，2026-10-26

- 私人帳號版顯示名稱改為 `English Learning Tool-alpha`，保留原 plugin 身分、package name 與全部 skill。
- 帳號封裝採獨立副本，更新及讀回比對均使用該副本；未來更新保留 `-alpha` 後綴。
- 完整讀回 6 個檔案，比對通過；skill 內容未變，未重跑語言案例。

這是帳號顯示資訊的 patch 修訂；repo manifest 保持 `0.1.2`，GitHub 安裝的 `0.1.0`、名稱及固定 ref 保留原樣。

## 0.1.2 — 私人帳號更新，2026-10-26

- 遷移並重新命名為 `english-back-translation`，保留繁中準備、逐輪回譯、回饋、每段原文比較、新情境運用與明確收尾。
- 精簡來源設計術語，補上明確選取、同對話續接、素材指令及換題邊界；不儲存學習紀錄或要求其他 skill。
- 修正既有兩個 skill 的整包用途澄清，涵蓋回譯練習；同步 manifest、catalog 描述與使用說明。

依使用者本次要求僅升 patch；不改變一般新能力升 minor 的維護約定。此版本已套用私人帳號並完成全部檔案讀回比對；個人 CLI 固定來源尚未切版，也未發布公開版本。驗證結果見[回譯驗證](docs/validation/back-translation.md)。

## 0.1.1 — 私人帳號更新，2026-10-26

- 將插件描述與顯示資訊改為英語學習工具集合，列出目前包含的獨立工具。
- README 先提供最短指令與一次設定後只貼內容的連續使用方式。
- 新增來源／實際 ZIP 檢查、拒絕重複鍵的 JSON／YAML 解析與輕量 CI。
- 新增只輸出固定欄位差異的帳號比對工具；工具探索改為先投影名稱。

本項描述私人帳號修訂，不代表已發布公開 tag 或 GitHub Release。兩份 skill 的語言行為保持不變。

## Unreleased — 0.1.0 準備中

- 將英文翻譯與句型講解整合為一個 skills-first plugin，各保留獨立入口。
- 精簡從 GPTs 轉換而來的命名、重複規則與空殼，保留三版翻譯、完整例句密度及當次要求優先。
- 兩平台共用 skills，提供必要 manifest 與指向同 checkout 的 catalog。
- 補上固定來源安裝、更新限制、維護流程與逐平台驗證紀錄。
- 補上私人帳號版的 OpenAI 顯示資訊；完成 Codex 個人環境與 ChatGPT 網頁核心驗證，解除安裝兩個舊插件。

尚未建立 `v0.1.0` tag 或 GitHub Release。Codex CLI 的已測行為、Claude 與桌面的待補項目見[驗證總覽](docs/verification.md)。
