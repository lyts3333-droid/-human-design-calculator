# 安裝 Git 步驟指南

## 📥 下載 Git

### 方法 1：官方網站下載（推薦）

1. **打開瀏覽器**，訪問：
   ```
   https://git-scm.com/download/win
   ```

2. **頁面會自動開始下載** Git for Windows
   - 如果沒有自動下載，點擊下載按鈕

3. **等待下載完成**（通常幾十MB，很快）

---

## 🔧 安裝 Git

1. **找到下載的文件**（通常在「下載」資料夾）
   - 文件名類似：`Git-2.xx.x-64-bit.exe`

2. **雙擊安裝文件**開始安裝

3. **按照安裝嚮導進行**：
   - 點擊「Next」繼續
   - **許可證協議**：點擊「Next」
   - **選擇安裝位置**：使用默認位置，點擊「Next」
   - **選擇組件**：使用默認選項，點擊「Next」
   - **選擇開始菜單文件夾**：使用默認，點擊「Next」
   - **選擇默認編輯器**：選擇「Use Visual Studio Code as Git's default editor」（如果有的話），或使用默認，點擊「Next」
   - **調整 PATH 環境**：使用默認選項「Git from the command line and also from 3rd-party software」，點擊「Next」
   - **選擇 HTTPS 傳輸後端**：使用默認「Use the OpenSSL library」，點擊「Next」
   - **配置行結束符**：使用默認「Checkout Windows-style, commit Unix-style line endings」，點擊「Next」
   - **配置終端模擬器**：使用默認「Use MinTTY」，點擊「Next」
   - **選擇默認的「git pull」行為**：使用默認，點擊「Next」
   - **選擇憑證助手**：使用默認，點擊「Next」
   - **配置額外選項**：使用默認，點擊「Next」
   - **配置實驗性選項**：不勾選任何選項，點擊「Install」
   - **等待安裝完成**：點擊「Finish」

---

## ✅ 驗證安裝

1. **關閉當前的命令提示符窗口**（重要！）

2. **重新打開命令提示符**：
   - 按 `Win + R`
   - 輸入 `cmd`
   - 按 Enter

3. **檢查 Git 是否安裝成功**：
   ```bash
   git --version
   ```

4. **如果顯示版本號**（例如 `git version 2.43.0`）：
   - ✅ **安裝成功！** 可以繼續下一步

5. **如果還是顯示錯誤**：
   - 可能需要重新啟動電腦
   - 或檢查安裝是否完成

---

## 🎯 安裝完成後

安裝完成後，請告訴我，我會繼續指導您：
1. 初始化 Git 倉庫
2. 提交文件
3. 推送到 GitHub
4. 在 Netlify 連接

---

## 💡 提示

- **安裝過程約 5-10 分鐘**
- **使用默認選項即可**，不需要修改
- **安裝完成後必須重新打開命令提示符**，否則 Git 命令無法使用

