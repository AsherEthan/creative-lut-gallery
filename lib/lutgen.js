// lutgen.js — 創意風格 LUT 圖鑑的參數模型（與網站使用同一套演算法）
// 用法：import { fetchLook, generateCube } from './lutgen.js';
//       const look = await fetchLook('kodak_2383'); const cube = generateCube(look, { size: 33, intensity: 0.8 });

export const API_BASE = 'https://asherethan.github.io/creative-lut-gallery/api';

export const DEFAULTS = { exp: 0, temp: 0, tint: 0, sat: 1, con: 1, piv: 0.45, lift: [0, 0, 0], gam: [1, 1, 1],
  gain: [1, 1, 1], sh: [0, 0, 0], hi: [0, 0, 0], fade: 0, roll: 1, mix: null, bw: null };

const cl = v => (v < 0 ? 0 : v > 1 ? 1 : v);

/** 回傳 (r, g, b) => [r, g, b]，輸入輸出皆為 0–1 的 Rec.709 顯示值 */
export function makeTransform(params = {}) {
  const P = { ...DEFAULTS, ...params };
  const em = Math.pow(2, P.exp);
  const wr = em * (1 + 0.12 * P.temp), wg = em * (1 - 0.08 * P.tint), wb = em * (1 - 0.12 * P.temp);
  const ig = P.gam.map(g => 1 / g), m = P.mix, bw = P.bw, c = P.con, pv = P.piv, s = P.sat, fd = P.fade, rg = P.roll - P.fade;
  const LI = P.lift, GA = P.gain, SH = P.sh, HI = P.hi;
  const sc = v => (v < pv ? pv * Math.pow(v / pv, c) : 1 - (1 - pv) * Math.pow((1 - v) / (1 - pv), c));
  const lg = (v, i) => { v = cl(GA[i] * (v + LI[i] * (1 - v))); return ig[i] === 1 ? v : Math.pow(v, ig[i]); };
  return (r, g, b) => {
    r *= wr; g *= wg; b *= wb;
    if (m) { const R = m[0] * r + m[1] * g + m[2] * b, G = m[3] * r + m[4] * g + m[5] * b, B = m[6] * r + m[7] * g + m[8] * b; r = R; g = G; b = B; }
    if (bw) { r = g = b = bw[0] * r + bw[1] * g + bw[2] * b; }
    r = cl(r); g = cl(g); b = cl(b);
    if (c !== 1) { r = sc(r); g = sc(g); b = sc(b); }
    let l = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    r = cl(l + (r - l) * s); g = cl(l + (g - l) * s); b = cl(l + (b - l) * s);
    r = lg(r, 0); g = lg(g, 1); b = lg(b, 2);
    l = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    const ws = (1 - l) * (1 - l), wh = l * l;
    r += SH[0] * ws + HI[0] * wh; g += SH[1] * ws + HI[1] * wh; b += SH[2] * ws + HI[2] * wh;
    return [cl(fd + cl(r) * rg), cl(fd + cl(g) * rg), cl(fd + cl(b) * rg)];
  };
}

/** look：API 的風格 JSON（含 params）或參數物件。回傳 .cube 文字 */
export function generateCube(look, { size = 33, intensity = 1, decimals = 6 } = {}) {
  const fn = makeTransform(look.params || look), N = size, k = intensity;
  const title = String(look.name_en || look.id || 'Creative LUT').replace(/[^\x20-\x7e]/g, '').replace(/"/g, "'").trim() || 'Creative LUT';
  const L = [`TITLE "${title}"`, '# Creative LUT approximation - Creative LUT Gallery',
    `# Input: Rec.709 display-referred. Intensity: ${Math.round(k * 100)}%`, `LUT_3D_SIZE ${N}`,
    'DOMAIN_MIN 0.0 0.0 0.0', 'DOMAIN_MAX 1.0 1.0 1.0'];
  for (let b = 0; b < N; b++) for (let g = 0; g < N; g++) for (let r = 0; r < N; r++) {
    const R = r / (N - 1), G = g / (N - 1), B = b / (N - 1), o = fn(R, G, B);
    L.push([R + (o[0] - R) * k, G + (o[1] - G) * k, B + (o[2] - B) * k].map(v => v.toFixed(decimals)).join(' '));
  }
  return L.join('\n') + '\n';
}

/** 直接套用到 Canvas 的 ImageData（原地修改） */
export function applyToImageData(imageData, look, intensity = 1) {
  const fn = makeTransform(look.params || look), d = imageData.data;
  for (let i = 0; i < d.length; i += 4) {
    const r = d[i] / 255, g = d[i + 1] / 255, b = d[i + 2] / 255, o = fn(r, g, b);
    d[i] = (r + (o[0] - r) * intensity) * 255; d[i + 1] = (g + (o[1] - g) * intensity) * 255; d[i + 2] = (b + (o[2] - b) * intensity) * 255;
  }
  return imageData;
}

export async function fetchLooks() { return (await fetch(`${API_BASE}/looks.json`)).json(); }
export async function fetchLook(id) { return (await fetch(`${API_BASE}/looks/${id}.json`)).json(); }
