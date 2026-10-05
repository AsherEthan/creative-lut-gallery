# 創意風格 LUT 圖鑑 · Creative LUT Gallery

收錄 **327 種**創意風格 LUT，涵蓋電影底片、印片模擬、攝影底片、相機原廠風格、手機／App 濾鏡、經典電影、劇集、亞洲影視、動畫、沖印工藝、年代、類型片、季節天氣、社群流行色和黑白。

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
| `GET /moods.json` | 情緒分類體系和各標籤數量 |
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
  "emotions": ["懷舊", "史詩", "神秘"],
  "valence": 0.1,
  "arousal": 0.15,
  "quadrant": "正向高能",
  "color": {"temperature": "冷暖分離", "saturation": "中飽和", "contrast": "中對比", "key": "中間調"},
  "scenes": ["人像", "夜景", "街拍"],
  "styles": ["電影感", "復古"],
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


## 情緒標註（v1.1）

每個風格都用四個獨立維度標註，可以自由組合篩選：

| 欄位 | 說明 | 可能的值 |
|---|---|---|
| `emotions` | 1–3 個情緒，依貼切程度排序 | 正向高能：興奮、歡快、熱烈、活力<br>正向低能：寧靜、溫馨、治癒、浪漫<br>負向高能：緊張、恐懼、不安、憤怒<br>負向低能：憂鬱、孤獨、荒涼、疏離<br>複合：懷舊、夢幻、神秘、史詩 |
| `valence` | 效價，-1（負向）到 1（正向） | 數值 |
| `arousal` | 喚醒度，-1（平靜）到 1（激烈） | 數值 |
| `quadrant` | 由 valence、arousal 決定的象限 | 正向高能、正向低能、負向高能、負向低能 |
| `color` | 由 LUT 參數實際計算 | temperature：暖調／冷調／冷暖分離／中性<br>saturation：高飽和／中飽和／低飽和／黑白<br>contrast：高對比／中對比／低對比<br>key：亮調／中間調／暗調 |
| `scenes` | 適用場景 | 人像、風景、夜景、街拍、室內、美食／產品 |
| `styles` | 風格 | 寫實、復古、底片感、電影感、實驗 |

完整詞表和各標籤的數量見 `GET /moods.json`。`tags` 是舊版標籤，保留以維持相容。

> 色彩屬性是算出來的；情緒、場景、風格是依作品基調判斷的建議值，不是絕對答案。

```python
import json, urllib.request
looks = json.load(urllib.request.urlopen("https://asherethan.github.io/creative-lut-gallery/api/api/looks.json"))["looks"]
# 憂鬱 + 冷調 + 夜景
picks = [l for l in looks
         if "憂鬱" in l["emotions"] and l["color"]["temperature"] == "冷調" and "夜景" in l["scenes"]]
# 最平靜又最正向的 5 個
calm = sorted(looks, key=lambda l: l["arousal"] - l["valence"])[:5]
```
