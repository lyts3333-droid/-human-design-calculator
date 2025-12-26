# Netlify 部署步驟指南

## 📋 前置準備

### 步驟 1：確認文件已準備好

請確認以下文件存在：

1. ✅ `netlify.toml` - 在根目錄
2. ✅ `index_netlify.html` - 在根目錄  
3. ✅ `netlify/functions/calculate_hd/__init__.py` - Function 代碼
4. ✅ `netlify/functions/requirements.txt` - Python 依賴
5. ✅ `.gitignore` - Git 忽略文件（已配置好）

**檢查方法**：在文件瀏覽器中查看您的「人類圖」資料夾，確認這些文件存在。

---

## 🚀 部署步驟

### 步驟 2：登入 Netlify

1. 打開瀏覽器，訪問：https://app.netlify.com
2. 點擊「Sign up」或「Log in」
3. 選擇登入方式：
   - 使用 **GitHub** 帳號（推薦）
   - 或使用 **GitLab** 帳號
   - 或使用 **Bitbucket** 帳號
   - 或使用 **Email** 註冊新帳號

---

### 步驟 3：連接 Git 倉庫（如果還沒有）

**如果您還沒有 Git 倉庫：**

1. 在 GitHub/GitLab/Bitbucket 創建新倉庫
2. 在本地執行：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <您的倉庫URL>
   git push -u origin main
   ```

**如果您已經有 Git 倉庫：**

跳過此步驟，直接到步驟 4。

---

### 步驟 4：在 Netlify 中導入項目

1. 在 Netlify Dashboard 中，點擊 **「Add new site」**
2. 選擇 **「Import an existing project」**
3. 選擇您的 Git 提供者（GitHub、GitLab 或 Bitbucket）
4. 如果是第一次使用，會要求授權，點擊 **「Authorize Netlify」**
5. 選擇包含「人類圖」項目的倉庫

---

### 步驟 5：配置構建設置

Netlify 應該會自動檢測到 `netlify.toml` 配置文件。

**檢查這些設置是否正確：**

- **Build command**: 
  ```
  cp -f index_netlify.html index.html && echo 'index.html updated for Netlify' || echo 'Warning: Could not copy index_netlify.html'
  ```
  或者 Netlify 可能顯示其他命令（只要來自 `netlify.toml` 就可以）

- **Publish directory**: 
  ```
  .
  ```
  （點號表示根目錄）

- **Functions directory**: 
  ```
  netlify/functions
  ```

如果這些設置正確，直接點擊 **「Deploy site」**

如果設置不對，請手動輸入上面的值，然後點擊 **「Deploy site」**

---

### 步驟 6：等待部署完成

1. 部署通常需要 **1-2 分鐘**
2. 您會看到部署進度：
   - 「Installing dependencies」
   - 「Building」
   - 「Deploying」
3. 等待直到看到 **「Deploy successful!」** 或 **「Published」**

---

### 步驟 7：訪問您的網站

部署完成後：

1. Netlify 會提供一個網址，例如：
   ```
   https://your-site-name-12345.netlify.app
   ```
2. 點擊這個網址，或複製到瀏覽器中打開
3. 您應該看到人類圖計算器的頁面

---

### 步驟 8：測試功能

1. 在網站上輸入出生資料：
   - 年份：例如 2002
   - 月份：例如 9
   - 日期：例如 21
   - 時間：例如 01:31
   - 縣市：選擇一個（例如 臺中市）
   - 區域：選擇一個（例如 西屯區）

2. 點擊 **「計算人類圖」** 按鈕

3. 應該會顯示計算結果

---

## ⚠️ 如果部署失敗

### 檢查構建日誌

1. 在 Netlify Dashboard 中，點擊失敗的部署
2. 點擊 **「View deploy log」**
3. 查看錯誤信息

### 常見問題

**問題 1：構建命令失敗**
- 檢查 `netlify.toml` 文件是否存在
- 確認構建命令是否正確

**問題 2：找不到 index.html**
- 確認 `index_netlify.html` 文件存在
- 檢查構建命令是否成功執行

**問題 3：Function 404 錯誤**
- 檢查 `netlify/functions/calculate_hd/__init__.py` 是否存在
- 確認 `netlify.toml` 中 Functions 目錄設置正確

### 清除緩存並重新部署

1. 在 Netlify Dashboard 中
2. 點擊 **「Deploys」** 標籤
3. 點擊 **「Trigger deploy」** → **「Clear cache and deploy site」**

---

## ✅ 完成檢查清單

部署成功後，請確認：

- [ ] 網站可以正常訪問
- [ ] 頁面顯示正常
- [ ] 可以輸入資料
- [ ] 計算功能正常工作
- [ ] 沒有錯誤信息

---

## 🎉 完成！

如果以上步驟都完成，您的網站就已經成功部署到 Netlify 了！

---

## 📞 需要幫助？

如果遇到問題：
1. 查看 Netlify 構建日誌
2. 檢查錯誤信息
3. 參考 `NETLIFY_TROUBLESHOOTING.md` 文檔

