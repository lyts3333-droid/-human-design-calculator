# 在 Web 版（Vercel）啟用資料庫與帳號登入

目前程式已支援：**在 Vercel 上設定雲端資料庫後，即可使用「註冊／登入」與「歷史記錄」**。

## 一、為什麼需要雲端資料庫？

- Vercel 的 Serverless 無法使用本機檔案（例如 SQLite），所以必須使用**雲端資料庫**。
- 設定好後，訪客打開網站會先看到**登入／註冊畫面**，註冊帳號密碼後即可登入，歷史記錄會存在雲端資料庫。

## 二、建議使用：Neon（免費方案）

1. **註冊 Neon**
   - 打開：https://neon.tech  
   - 用 GitHub 或 Email 註冊，建立一個新專案（例如名稱：`human-design`）。

2. **取得連線字串**
   - 在 Neon 專案裡點 **Connection string** 或 **Dashboard → Connection details**。
   - 複製 **PostgreSQL** 連線字串，長相類似：
     ```text
     postgresql://使用者:密碼@ep-xxx.region.aws.neon.tech/資料庫名?sslmode=require
     ```

3. **在 Vercel 設定環境變數**
   - 打開 https://vercel.com/dashboard → 點進你的專案 **human-design-calculator**。
   - 上方選 **Settings** → 左側 **Environment Variables**。
   - 新增一筆：
     - **Name**：`DATABASE_URL`
     - **Value**：貼上剛才複製的 Neon 連線字串。
     - 環境勾選 **Production**（若有 Preview 也可勾）。
   - 儲存後，到 **Deployments** 對最新一次部署點 **Redeploy**，讓新環境變數生效。

4. **（可選）設定 SECRET_KEY**
   - 建議再新增一筆環境變數：
     - **Name**：`SECRET_KEY`
     - **Value**：一串隨機字串（例如用密碼產生器產生 32 字元以上）。
   - 用於 session 加密，提高安全性。

## 三、設定完成後的行為

- 再次打開 **https://human-design-calculator.vercel.app** 會先進入**登入／註冊**畫面。
- 訪客可點「註冊」建立帳號密碼，之後用「登入」進入。
- 登入後可正常使用人類圖計算，**歷史記錄會寫入雲端資料庫**並在「歷史記錄」中顯示。

## 四、若未設定 DATABASE_URL

- 行為與現在一樣：**不會出現登入畫面**，直接進入主畫面，歷史記錄僅存在瀏覽器（localStorage），不會存到伺服器。

## 五、其他雲端資料庫（可選）

- **Supabase**：https://supabase.com → 建立專案後，在 Settings → Database 取得 **Connection string (URI)**，一樣設成 Vercel 的 `DATABASE_URL`。
- **Vercel Postgres（透過 Marketplace）**：若 Vercel 有提供 Postgres 整合，連線字串通常會自動注入為 `DATABASE_URL` 或 `POSTGRES_URL`，程式已支援這兩種變數名稱。

---

總結：在 Vercel 專案裡加上 **DATABASE_URL**（指向 Neon 或其他 Postgres），重新部署後，Web 版就會有資料庫並支援註冊／登入與歷史記錄。
