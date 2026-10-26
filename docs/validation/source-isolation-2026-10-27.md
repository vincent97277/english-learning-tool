# 來源隔離、完整練習與 GitHub 更新驗收

日期：2026-10-27。依[本輪規格](../../.scratch/source-isolation-20261027/spec.md)，review 基準為 `1d92516`。候選封裝、隔離驗收與正式安裝分開記錄。

## 實際個人來源與名稱碰撞

正式設定的原生 `plugin/list` 明確查詢 local／created-by-me-remote catalog、forceRefetch，再以 `skills/list` forceReload 重新掃描；沒有用隔離副本代替正式安裝。

| 狀態 | GitHub | 帳號 | enabled 入口／同名組數 |
| --- | --- | --- | --- |
| 更新前的個人設定 | 0.1.0，固定 `4943067` | 0.1.3，顯示名含 alpha | 5／2，translator、patterns |
| 本輪更新後的個人設定 | 0.1.2，固定 `8e9abb2` | 仍為 0.1.3 | 6／3，含 back-translation |
| 隔離候選，同時安裝兩來源 | 0.1.2 canonical 入口 | 0.1.4，三個 `*-alpha` 入口 | 6／0 |

因此只有 plugin 顯示名稱帶 `-alpha`，不能唯一區分 skill。正式帳號尚未改名，實際個人環境的碰撞仍存在；不能宣稱已消除誤選風險。

隔離測試先使用帳號 0.1.3／GitHub 候選 0.1.2 重現三組碰撞，唯一名稱檢查非零失敗。`account-source` 只改帳號副本的顯示名稱、版本、三個 skill 目錄及 frontmatter 名稱，保留正文與 package 身分；改用候選帳號副本後同一 discovery 檢查為零碰撞。

## 模型驗收

使用 Codex CLI 0.162.1／模型回報 gpt-6.1-sol。兩份來源以不含 alpha／GitHub 提示的 registry-a／registry-b local marketplace 安裝到隔離設定；內容取自實際帳號來源或本輪候選。空工作目錄、ephemeral、read-only、approval never；停用 apps 與 remote_plugin，且不繼承桌面 task identity／工具 bridge。暫存登入連結結束移除，原認證保留；全部為合成素材。

明確選取傳入 discovery 的 name／path，檢查 host 回傳 userMessage 包含同一 name／path。自然語言指定來源則另外檢查實際讀檔命令。不以模型自述或兩來源產出相同翻譯推定來源。

| 已完成案例 | 觀察結果 |
| --- | --- |
| 明確選取 GitHub translator，要求單版翻譯 | 一版英文，保留不確定性及「不要等我」的否定。 |
| 明確選取 alpha patterns，要求簡短、兩個雙語例句 | 繁中說明、恰兩個附中譯例句；host 確認 alpha name／path。 |
| 純文字要求用 English Learning Tool-alpha 翻譯 | 實際讀取的來源為 english-translator-alpha；產出單版英文。 |
| plugin 顯示名稱後綴管理負例 | 說明 alpha 標示，未進入翻譯／句型教學或修改檔案。 |
| GitHub 回譯同一 thread：AI 繁中出題、錯誤作答、自修、原文比較、新情境作答 | 逐輪等待；提示 had + 過去分詞後等待自修；正確修訂後說明原文選擇；新情境只回答後悔句時，保留原成功部分，追問尚缺的「今天很累」。共四個實際回合 completed，未把未結束的練習列為完整收尾通過。 |

首輪共八個模型回合 completed。補做收尾的同一 thread 另四回合 completed：出題 → 錯誤作答及自修提示 → 正確修訂及來源比較／新情境 → 含「今天很累」的完整作答。模型接受後悔句，指出 so 把 wish 接成疲累原因的連接問題，示範分成兩句；明確宣布練習完成、後續練習可選，並標示中文由 AI 提供、自修及新情境均獲提示／句型支援，沒有宣稱獨立熟練。兩輪合計十二個行為回合 completed；控制回合另計。

來源副本的隔離驗收不代表 remote marketplace 更新 lifecycle 或原生桌面 `@` 點選已實測。沒有指定來源的自然語言任務可選任一適用來源；六個唯一名稱不保證所有未測意圖均正確。

## 限流與未完成回合

先前兩份逾時 transport log 顯示 HTTP 429，要求約 562／420 秒重試，長於當時 90 秒截止時間。這些舊回合仍未完成，不改列為通過。新工具保留所有通知，按 thread／turn ID 配對完成事件，並記錄 transport 狀態；同一 thread 的 CONTROL_ONE／CONTROL_TWO 控制回合均 completed。

本輪首輪回譯遇到約 552 秒退避後完成。補做收尾時，一次沙盒網路失敗為 workspace routing discovery failed，未產生模型輸出；恢復正常網路後重新測試，遇到約 411 秒服務退避，依要求等待後完成四個回合。環境錯誤不判為 skill 行為通過或失敗。

## 靜態檢查、review 與部署

- 14 項測試通過。`account-source` 命令先在不存在時失敗，實作後通過；從既有 alpha 副本再次派生原先產生 alpha-alpha，新增拒絕規則後通過。GitHub 原來源逐位元保持不變。
- Spec review 重現 compatibility manifest 的 skills 路徑變更會漏報；新增錯誤路徑／未知欄位測試先失敗，再補上完整內容比對，既有帳號 0.1.3 完整讀回仍通過。輸出不含原始帳號值。
- GitHub 及帳號候選的來源／實際 ZIP 檢查通過。GitHub `8e9abb226c17a26c6c3cb535871e53a8f2ceb7eb` 已推送，GitHub Actions 通過；個人 CLI 已透過官方 marketplace 移除／固定 ref 重新登記／安裝流程切至該 commit 的 0.1.2。事前確認來源只有本 plugin，僅保存它的來源及啟用設定。
- 安裝後根 manifest、LICENSE、三個 skill 共五檔，在來源快照及 discovery 回傳的安裝快取均逐位元符合固定 commit；三個 GitHub skill enabled。帳號來源及其他 marketplace 未變。
- Standards review 為 0 findings。Spec review 的一項 P2 已修正，針對修正複審後無未解問題；兩軸 review 不替代待補的平台驗收。
- [PR #1](https://github.com/vincent97277/english-learning-tool/pull/1) 承載 GitHub 更新。未建立公開 tag 或 GitHub Release。

帳號正式更新仍受阻：自動核准審查拒絕刪除被新 alpha 檔案取代的三個舊 SKILL.md 路徑，未接受先前名稱修正授權。已請使用者明確確認帳號 0.1.4 更新及舊路徑替換；目前正式帳號仍為 0.1.3，不以新增另一 plugin、保留舊入口或直接改快取繞過。候選 0.1.4 ZIP 並未部署。

原生桌面 `@` 選單未手動驗證；本輪不作零誤用保證。
