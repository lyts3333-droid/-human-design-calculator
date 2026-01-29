# CSV文件位置說明

## 文件位置要求

`基因天命.csv` 文件**必須**與 `index.html` 放在**同一個目錄**中。

## 正確的文件結構

```
人類圖/
├── index.html          ← HTML文件
├── 基因天命.csv        ← CSV文件（必須在同一目錄）
├── app.py
└── 其他文件...
```

## 部署到Vercel時的注意事項

1. **確保CSV文件被Git追蹤**：
   - CSV文件必須在Git倉庫中
   - 執行 `git add 基因天命.csv` 將文件添加到Git
   - 執行 `git commit` 和 `git push` 上傳到GitHub

2. **Vercel會自動部署**：
   - 當您推送到GitHub時，Vercel會自動部署
   - CSV文件會與index.html一起部署到同一目錄

3. **訪問路徑**：
   - 在Vercel上，可以使用 `/基因天命.csv` 訪問
   - 或者使用相對路徑 `./基因天命.csv`

## 檢查文件是否正確上傳

1. 在GitHub上查看您的倉庫
2. 確認 `基因天命.csv` 文件存在於 `人類圖/` 目錄中
3. 在Vercel部署日誌中確認文件被包含

## 如果仍然找不到文件

請確認：
1. ✅ CSV文件與index.html在同一目錄
2. ✅ CSV文件已被Git追蹤（執行 `git status` 檢查）
3. ✅ CSV文件已推送到GitHub
4. ✅ Vercel部署包含該文件

## 當前文件位置

根據檢查，您的CSV文件已經在正確的位置：
- 文件路徑：`人類圖/基因天命.csv`
- 與 `index.html` 在同一目錄 ✅



