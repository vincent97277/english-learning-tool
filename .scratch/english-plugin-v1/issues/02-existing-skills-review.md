# 既有兩項 skill 應保留什麼、精簡什麼？

Type: research
Labels: wayfinder:research
Status: resolved
Assignee: vincent97277
Parent: ../map.md
Blocked by: none

## Question

以目前安裝的 English Patterns 0.8.0、English Translator 0.13.0 為來源，哪些行為是應保留的產品契約，哪些 GPTs 轉換痕跡、重複描述、觸發衝突或過長預設值得調整？請提出最小改善清單與小型合成驗收案例，特別處理三版翻譯、句型例句數量、局部追問、混合要求與引用內命令。不直接改寫或遷移來源 skill。

註明來源版本與公開再利用／MIT 標示的已知邊界，不納入私人內容或授權來源不明的圖示。所有會改變使用者習慣的建議須標為待人類確認。

## Assets

- [既有行為 review 報告](https://github.com/vincent97277/english-learning-tool/blob/d78df68d11441f65f04a7e05b739f42c4c907e44/docs/research/existing-skills-review.md)，保存在 `research/existing-skills-review`，未開 PR、未合併。

## Answer

2026-10-26：已完成已安裝版本的靜態 review。既有任務邊界、素材內指令處理、混合要求與續問規則成熟，應保留；最小改善為區分兩個 `instructions` 名稱、精簡重複描述、移除空索引與 GPT ID，不增加路由層。候選 skill 名稱為 `english-patterns`／`english-translator`，尚非已發布識別名稱。

翻譯預設三版與句型例句密度為體驗偏好，留待[初版要保留哪些輸出與互動行為？](04-behavior-contract.md)與使用者確認。原 PNG 缺來源證據，初版建議不搬。報告以版本、相對檔案行號和 SHA256 識別舊來源，未將私人安裝目錄收進 repo；其中十個合成驗收案例尚未執行。內容精簡建議尚未實作，也不等於兩平台行為通過。
