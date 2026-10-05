# 創意風格 LUT 圖鑑 · Creative LUT Gallery

收錄 **253 種**創意風格 LUT，涵蓋電影底片、印片模擬、攝影底片、相機原廠風格、手機／App 濾鏡、經典電影、劇集、亞洲影視、動畫、沖印工藝、年代、類型片、季節天氣、社群流行色和黑白。

- 🌐 **網站**：https://asherethan.github.io/creative-lut-gallery/ —— 上傳照片即時預覽、左右拖動比較、調整強度、下載 33³ `.cube`
- 🔌 **靜態 JSON API**：架在 GitHub Pages 上，免金鑰，可以跨網域呼叫
- 🧰 **產生器**：JS 和 Python，可自訂網格尺寸（17／33／65）和強度

> ⚠️ 所有 LUT 都是依各風格公開可見的特徵（色溫、對比、飽和度、分離色調、通道混合等），以參數重建的近似版本，**不是**原廠或電影製作方的檔案。品牌和片名只用來描述風格。

## API

Base URL：`https://asherethan.github.io/creative-lut-gallery/api`

| 端點 | 說明 |
|---|---|
| `GET /index.json` | API 說明、版本、端點清單、參數模型 |
| `GET /looks.json` | 所有風格的摘要清單 |
| `GET /looks/{id}.json` | 單一風格的完整資料（含參數） |
| `GET /cube/{id}.cube` | 預先產生的 `.cube`（17³，強度 100%） |
| `GET /categories.json` | 分類和各分類數量 |
| `GET /sources.json` | 正版 LUT 來源整理 |

### 範例

```bash
curl https://asherethan.github.io/creative-lut-gallery/api/looks.json
curl -O https://asherethan.github.io/creative-lut-gallery/api/cube/kodak_2383.cube
```

```js
import { fetchLook, generateCube } from 'https://asherethan.github.io/creative-lut-gallery/lib/lutgen.js';
const look = await fetchLook('teal_orange');
const cube = generateCube(look, { size: 33, intensity: 0.8 }); // 33³、強度 80%
```

```python
import json, urllib.request
looks = json.load(urllib.request.urlopen("https://asherethan.github.io/creative-lut-gallery/api/looks.json"))["looks"]
print(len(looks), looks[0]["name"])
```

### 單一風格的資料格式

```json
{
  "id": "kodak_2383",
  "name": "Kodak 2383 印片",
  "name_en": "Kodak 2383 Print Film",
  "category": "pfe",
  "category_name": "印片模擬",
  "tags": ["戲劇", "溫暖"],
  "description": "…",
  "reference": "…",
  "source_type": "builtin",
  "where_to_find": "…",
  "params": { "exp": 0, "temp": 0, "con": 1.18, "sat": 1.05, "sh": [-0.02, 0.01, 0.025], "...": "..." },
  "cube_url": "https://asherethan.github.io/creative-lut-gallery/api/cube/kodak_2383.cube"
}
```

## 參數模型

所有風格都由同一組參數描述，處理順序如下（輸入輸出都是 0–1 的 Rec.709 顯示值）：

| 順序 | 參數 | 預設 | 作用 |
|---|---|---|---|
| 1 | `exp` | 0 | 曝光（檔數，×2^exp） |
| 1 | `temp` / `tint` | 0 | 色溫（藍↔黃）／色調（綠↔洋紅） |
| 2 | `mix` | null | 3×3 通道混合矩陣（列優先） |
| 3 | `bw` | null | 黑白權重 `[r, g, b]` |
| 4 | `con` / `piv` | 1 / 0.45 | 以 `piv` 為支點的 S 曲線對比 |
| 5 | `sat` | 1 | 飽和度 |
| 6 | `lift` / `gain` / `gam` | 0 / 1 / 1 | 各通道的 Lift、Gain、Gamma |
| 7 | `sh` / `hi` | 0 | 暗部／亮部的分離色調 `[r, g, b]` |
| 8 | `fade` / `roll` | 0 / 1 | 黑位抬升／白位壓縮 |

## 本地產生高精度 .cube

```bash
python tools/build_cubes.py --size 33 --out cubes                  # 全部 33³
python tools/build_cubes.py --size 65 --intensity 0.7 --ids kodak_2383 teal_orange
python tools/build_cubes.py --remote --size 33                     # 不用 clone，直接讀線上 API
```

只用 Python 標準函式庫，不用安裝任何套件。

## 使用提醒

1. Log 素材要先轉成 Rec.709，再套這些創意 LUT。
2. 套 LUT 之前先調好曝光和白平衡。
3. 強度通常 40%–80% 最自然。
4. 顆粒、暈光、暗角不是 LUT 能做的，需要另外加。

## 目錄結構

```
index.html              網站
api/                    靜態 JSON API 與 .cube
lib/lutgen.js           JS 產生器（ES module）
lib/lutgen.py           Python 產生器
tools/build_cubes.py    批次產生 .cube 的命令列工具
```

## 授權

程式碼以 MIT 授權釋出。風格名稱中提到的品牌、底片和電影名稱，版權歸各自的所有者。
