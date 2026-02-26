# Cursor 更新備份指南

## 📋 更新前的重要步驟

### ⚠️ 重要提醒
更新 Cursor 前，建議先備份對話記錄和項目文件，以防萬一。

---

## 🔄 對話記錄保留情況

### ✅ 通常會保留
- Cursor 的對話記錄通常保存在本地
- 更新時一般不會刪除對話歷史
- 但為了安全起見，建議先備份

### 📍 對話記錄存儲位置

**Windows 系統：**
```
C:\Users\<你的用戶名>\AppData\Roaming\Cursor\User\globalStorage\
```

或
```
C:\Users\<你的用戶名>\AppData\Roaming\Cursor\storage\
```

**macOS 系統：**
```
~/Library/Application Support/Cursor/User/globalStorage/
```

**Linux 系統：**
```
~/.config/Cursor/User/globalStorage/
```

---

## 💾 備份步驟

### 方法 1：備份整個項目（推薦）

1. **複製整個項目文件夾**
   - 找到項目位置：`C:\Users\a0929\OneDrive\桌面\CURSOR\人類圖`
   - 複製整個文件夾到安全位置（例如：另一個硬盤、雲端硬盤）

2. **或使用 Git 備份（最佳）**
   ```bash
   # 確保所有更改已提交
   git add .
   git commit -m "更新前備份"
   git push
   ```
   這樣即使本地文件丟失，也可以從 GitHub 恢復。

### 方法 2：備份 Cursor 配置和對話記錄

1. **找到 Cursor 數據文件夾**
   - 按 `Win + R`
   - 輸入：`%APPDATA%\Cursor`
   - 按 Enter

2. **備份以下文件夾：**
   - `User\globalStorage\` - 包含對話記錄
   - `User\settings.json` - 用戶設置
   - `User\keybindings.json` - 快捷鍵設置

3. **複製到安全位置**

### 方法 3：使用 Cursor 內建功能

1. **導出設置**
   - 打開 Cursor
   - 按 `Ctrl+Shift+P`（或 `Cmd+Shift+P` on Mac）
   - 輸入：`Preferences: Open Settings (JSON)`
   - 複製設置內容

2. **導出工作區設置**
   - 在項目根目錄找到 `.vscode` 文件夾
   - 備份其中的設置文件

---

## 🚀 安全更新步驟

### 步驟 1：提交所有更改到 Git（最重要）

```bash
# 1. 檢查狀態
git status

# 2. 添加所有更改
git add .

# 3. 提交
git commit -m "更新 Cursor 前備份所有更改"

# 4. 推送到 GitHub
git push
```

### 步驟 2：備份項目文件夾

1. 複製整個項目文件夾到另一個位置
2. 或上傳到雲端硬盤（OneDrive、Google Drive 等）

### 步驟 3：更新 Cursor

1. **自動更新：**
   - Cursor 通常會自動提示更新
   - 點擊「更新」按鈕即可

2. **手動更新：**
   - 訪問 Cursor 官網下載最新版本
   - 安裝時選擇「更新」而非「卸載後安裝」

### 步驟 4：更新後檢查

1. **檢查項目是否正常打開**
2. **檢查對話記錄是否還在**
3. **檢查設置是否保留**

---

## 🔧 如果對話記錄丟失

### 恢復方法 1：從備份恢復

1. 找到之前備份的 `globalStorage` 文件夾
2. 複製回 Cursor 的數據目錄

### 恢復方法 2：從 Git 恢復代碼

```bash
# 如果代碼丟失，從 GitHub 克隆
git clone https://github.com/你的用戶名/你的倉庫名.git
```

### 恢復方法 3：檢查 Cursor 的備份文件

Cursor 可能會自動創建備份，檢查：
```
%APPDATA%\Cursor\User\workspaceStorage\
```

---

## 📝 更新前檢查清單

- [ ] 所有代碼更改已提交到 Git
- [ ] 已推送到 GitHub（遠程倉庫）
- [ ] 已備份項目文件夾
- [ ] 已備份 Cursor 設置（可選）
- [ ] 已記錄重要的對話內容（可選）

---

## 💡 最佳實踐建議

### 1. 定期提交到 Git
```bash
# 每天結束工作前
git add .
git commit -m "今日工作進度"
git push
```

### 2. 使用 Git 作為主要備份
- GitHub 是免費的雲端備份
- 可以恢復任何歷史版本
- 不會因為本地問題丟失代碼

### 3. 重要對話內容可以保存
- 複製重要的對話內容到 Markdown 文件
- 保存在項目文件夾中
- 例如：`對話記錄.md`

---

## 🆘 遇到問題時

### 如果更新後對話記錄消失：

1. **不要驚慌** - 代碼還在（如果已提交到 Git）
2. **檢查備份** - 查看之前備份的文件
3. **重新開始對話** - Cursor 的 AI 可以根據代碼上下文繼續幫助你

### 如果項目文件丟失：

1. **從 Git 恢復：**
   ```bash
   git clone https://github.com/你的倉庫地址.git
   ```

2. **從雲端硬盤恢復**（如果有備份）

---

## 📞 需要幫助？

如果更新後遇到問題：
1. 檢查 Cursor 官方文檔
2. 查看 Cursor 社區論壇
3. 聯繫 Cursor 支持

---

**記住：最重要的備份是 Git！確保所有代碼都已提交並推送到 GitHub！**


