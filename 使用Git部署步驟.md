# 使用 Git 部署到 Netlify - 詳細步驟

## 📋 步驟總覽

1. 安裝 Git（如果還沒有）
2. 初始化 Git 倉庫
3. 提交文件
4. 在 GitHub/GitLab 創建遠程倉庫
5. 推送代碼
6. 在 Netlify 連接 Git 倉庫

---

## 步驟 1：檢查是否已安裝 Git

### Windows 用戶：

1. 按 `Win + R` 打開運行窗口
2. 輸入 `cmd` 並按 Enter
3. 在命令提示符中輸入：
   ```
   git --version
   ```

**如果顯示版本號**（例如 `git version 2.xx.x`）：
- ✅ Git 已安裝，跳到步驟 2

**如果顯示錯誤**（例如 'git' 不是內部或外部命令）：
- ❌ Git 未安裝，需要安裝

### 安裝 Git（如果沒有）：

1. 訪問：https://git-scm.com/download/win
2. 下載並安裝 Git for Windows
3. 安裝時使用默認選項即可
4. 安裝完成後重新打開命令提示符

---

## 步驟 2：初始化 Git 倉庫

1. **打開命令提示符**（cmd）或 **PowerShell**
2. **進入您的項目資料夾**：
   ```bash
   cd C:\Users\a0929\OneDrive\桌面\CURSOR\人類圖
   ```

3. **初始化 Git 倉庫**：
   ```bash
   git init
   ```

4. **檢查狀態**：
   ```bash
   git status
   ```

---

## 步驟 3：提交文件到 Git

1. **添加所有文件**：
   ```bash
   git add .
   ```

2. **提交文件**：
   ```bash
   git commit -m "準備 Netlify 部署"
   ```

---

## 步驟 4：創建 GitHub 帳號和倉庫（如果還沒有）

### 如果還沒有 GitHub 帳號：

1. 訪問：https://github.com
2. 點擊「Sign up」註冊新帳號
3. 按照提示完成註冊

### 創建新倉庫：

1. 登入 GitHub
2. 點擊右上角的 **「+」** → **「New repository」**
3. 填寫倉庫信息：
   - **Repository name**: `human-design-calculator`（或其他名稱）
   - **Description**: （可選）人類圖計算器
   - **Visibility**: 選擇 **Public**（公開）或 **Private**（私有）
   - **不要**勾選「Initialize this repository with a README」（因為我們已經有文件了）
4. 點擊 **「Create repository」**

---

## 步驟 5：連接到 GitHub 並推送代碼

GitHub 會顯示指令，但基本步驟是：

1. **添加遠程倉庫**（將 `YOUR_USERNAME` 和 `YOUR_REPO_NAME` 替換為您的實際值）：
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

2. **重命名分支為 main**（如果需要）：
   ```bash
   git branch -M main
   ```

3. **推送代碼到 GitHub**：
   ```bash
   git push -u origin main
   ```

4. **如果要求輸入帳號密碼**：
   - 用戶名：您的 GitHub 用戶名
   - 密碼：使用 **Personal Access Token**（不是 GitHub 密碼）
   - 獲取 Token：GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

---

## 步驟 6：在 Netlify 連接 Git 倉庫

1. **登入 Netlify**：https://app.netlify.com

2. **添加新網站**：
   - 點擊 **「Add new site」**
   - 選擇 **「Import an existing project」**

3. **連接 Git 提供者**：
   - 選擇 **GitHub**（或您使用的 Git 提供者）
   - 如果是第一次，會要求授權，點擊 **「Authorize Netlify」**

4. **選擇倉庫**：
   - 找到並選擇您剛創建的倉庫
   - 點擊它

5. **配置構建設置**：
   - Netlify 會自動檢測 `netlify.toml`
   - 確認設置正確後，點擊 **「Deploy site」**

6. **等待部署**：
   - 通常需要 1-2 分鐘
   - 等待看到 **「Deploy successful!」**

---

## ✅ 完成後

1. **訪問您的網站**：
   - Netlify 會提供一個網址
   - 例如：`https://your-site-name.netlify.app`

2. **以後更新代碼**：
   - 修改文件後，執行：
     ```bash
     git add .
     git commit -m "更新說明"
     git push
     ```
   - Netlify 會自動重新部署

---

## 🆘 如果遇到問題

### 問題 1：Git 命令不認識
- **解決**：確認已安裝 Git，或重新打開命令提示符

### 問題 2：無法推送到 GitHub
- **解決**：確認已正確添加遠程倉庫 URL
- **解決**：使用 Personal Access Token 作為密碼

### 問題 3：Netlify 找不到倉庫
- **解決**：確認已授權 Netlify 訪問 GitHub
- **解決**：確認倉庫名稱正確

### 問題 4：部署失敗
- **解決**：查看 Netlify 構建日誌
- **解決**：確認 `netlify.toml` 配置正確

---

## 💡 提示

- 每次修改代碼後，記得 `git add .`、`git commit`、`git push`
- Netlify 會自動檢測推送並重新部署
- 查看部署狀態在 Netlify Dashboard 的「Deploys」標籤

