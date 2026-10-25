# English Learning Tool

為 Claude Code 與 Codex 規劃的英語學習 plugin，以 skills 為主，初版聚焦英文翻譯與英文句型講解。

已完成研究與初版規格，下一階段進行實作，尚未提供可安裝的 plugin。決策與研究結果請見[初版決策地圖](.scratch/english-plugin-v1/map.md)。

[正式實作規格](.scratch/english-plugin-implementation/spec.md)已將[已確認的規劃](.scratch/english-plugin-v1/spec.md)整理為需求與驗收決定。工單切分已確認並發布，平台驗收仍須在實作階段執行。

依序處理以下實作工單；`ready-for-agent` 表示內容已具體定義，仍須遵守各票的前置依賴：

1. [在目標客戶端安裝並直接使用英文翻譯](.scratch/english-plugin-implementation/issues/01-translation.md)：無前置依賴，可立即開始。
2. [加入句型講解並正確切換兩個功能](.scratch/english-plugin-implementation/issues/02-patterns-and-switching.md)：依賴翻譯工單完成。
3. [交付固定版本安裝、更新驗收與發版準備](.scratch/english-plugin-implementation/issues/03-fixed-version-delivery.md)：依賴句型講解工單完成。

## 授權

本專案採用 [MIT License](LICENSE)。
