# 英文回譯練習遷移

Status: implemented
日期：2026-10-26。目標版本：`0.1.2`。

## Destination

將使用者授權的 back-translation-practice 納入目前 plugin，完成 repo 實作與受影響驗證。
使用者明確選擇本輪包含實作；名稱、保留流程及優化範圍已確認，路徑清楚且可在一輪完成，依 wayfinder 的小範圍例外不另建決策地圖。

## Confirmed decisions

- 新入口為 `english-back-translation`，顯示標題 English Back Translation，目錄與 frontmatter 同名。
- 保留英文素材、繁中準備、實際英文作答、回饋、逐段原文比較、一次新情境及準確結束的完整循環。
- 優化觸發與續接、素材指令邊界、正文表達；保留材料公平性、一次自修機會、直接求助、必要／可選修正及協助歸因。通用詞彙見 [GLOSSARY](../../GLOSSARY.md)。
- 同一對話接回實際待答階段，不虛構作答或永久學習紀錄；不要求其他 skill、帳號或服務。
- 兩個既有 skill 的整包澄清須涵蓋新能力，維持一次簡短詢問，不增加路由層或必經選單。
- 使用者明示僅迭代最小版號，本次由 `0.1.1` 升 patch `0.1.2`；這是本次新增能力的特例，不改寫維護流程的新能力升 minor 預設。
- 只遷移 runtime，不搬移來源的私人學習材料、歷史紀錄或維護工作區。來源專案維持原狀。

## Validation

執行既有測試、來源與實際 ZIP 檢查、skill validator，並用合成素材驗證新入口的逐輪等待、材料公平性、來源比較、直接求助、收尾與任務覆寫。可用客戶端驗收優先；獨立代理行為檢查與客戶端結果分別記錄，不以靜態檢查替代實測。

Repo 實作與封裝完成；客戶端完整三輪循環仍有完成事件逾時的待驗項，不因實作完成而宣稱通過。實際結果及限制見[回譯驗證](../../docs/validation/back-translation.md)。

## Out of scope

帳號插件更新、個人安裝切版、原專案刪除、舊 skill 停用、公開 tag、GitHub Release 與目錄上架不在本輪 repo 實作範圍。
