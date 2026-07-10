# -*- coding: utf-8 -*-
"""
منوی آنلاین رستوران - نسخه پایتون (Flask)
اجرا در Pydroid 3:
  1) از منوی Pydroid وارد Pip شو و پکیج flask رو نصب کن (pip install flask)
  2) این فایل رو اجرا کن (دکمه Run)
  3) توی مرورگر گوشی برو به آدرس: http://127.0.0.1:5000
داده‌ها (سرفصل‌ها، محصولات، رمز مدیر) توی فایل menu_data.json کنار همین اسکریپت ذخیره می‌شن.
"""

import json
import os
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "menu_data.json")


# ---------------------------------------------------------------------------
# ذخیره‌سازی ساده روی فایل JSON
# ---------------------------------------------------------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"categories": [], "password": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"categories": [], "password": None}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------
@app.route("/api/menu", methods=["GET"])
def get_menu():
    data = load_data()
    return jsonify({"categories": data.get("categories", [])})


@app.route("/api/menu", methods=["POST"])
def save_menu():
    body = request.get_json(force=True)
    data = load_data()
    data["categories"] = body.get("categories", [])
    save_data(data)
    return jsonify({"ok": True})


@app.route("/api/password/status", methods=["GET"])
def password_status():
    data = load_data()
    return jsonify({"exists": bool(data.get("password"))})


@app.route("/api/password/set", methods=["POST"])
def password_set():
    body = request.get_json(force=True)
    new_pass = (body.get("password") or "").strip()
    if len(new_pass) < 4:
        return jsonify({"ok": False, "error": "رمز باید حداقل ۴ کاراکتر باشد."}), 400
    data = load_data()
    if data.get("password"):
        return jsonify({"ok": False, "error": "رمز قبلاً تعیین شده است."}), 400
    data["password"] = new_pass
    save_data(data)
    return jsonify({"ok": True})


@app.route("/api/password/verify", methods=["POST"])
def password_verify():
    body = request.get_json(force=True)
    entered = body.get("password") or ""
    data = load_data()
    return jsonify({"ok": entered == data.get("password")})


@app.route("/api/tagline", methods=["GET"])
def get_tagline():
    data = load_data()
    return jsonify({"tagline": data.get("tagline", "Be kind with your taste")})


@app.route("/api/tagline", methods=["POST"])
def set_tagline():
    body = request.get_json(force=True)
    text = (body.get("tagline") or "").strip()
    data = load_data()
    data["tagline"] = text
    save_data(data)
    return jsonify({"ok": True})


@app.route("/api/uid", methods=["GET"])
def get_uid():
    # کمک به فرانت‌اند برای ساخت شناسه یکتا (اختیاری، جاوااسکریپت خودش هم می‌سازه)
    return jsonify({"uid": uuid.uuid4().hex})


# ---------------------------------------------------------------------------
# صفحه اصلی (HTML + CSS + JS در یک فایل)
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return HTML_PAGE


LOGO_B64 = (
    "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"
    "SVQKDE0gYIajlH0Z1J/0b3voP0ZErlrN0NOT3MtzXPgcZ3bNi9NGvaOjacWV6fskvBUMLw5ZgJJB"
    "SbPDAywOn5MhkFmADaWjoD5ixr84uH3H/eewFy54jguf48xiRsJ5V7x4zaLK8Wwzye+i7BXMwk0Q"
    "iiIwhRTYqDnViHNLo/5dCDYJlm8o0+cl/Wdk2PboacHzGqeOC5/jzMl50tUVhotfA8Dy5964jNnQ"
    "Swj8oKDnk6GJpZ9YVkMzCBrlEV6quSao+FQgI0gMp+yUgv2oqO0Qugeba59+/NN7jp1+Z4RR+3mO"
    "48LnOHNyvlSrEct6NEoQePmma1c2K74J4KsYuFKGRSGyGSRkAkwmKAdBqggqToMYFl6ZJPG06BKs"
    "MBAgi/As9DjFo5S+AOAfK1nbp/b29JwaeUpXV7Fv2d3t9TUdFz7Hcc45d06LQ3XVvCst64ipaW2I"
    "dhPAzRCuZuRyViJgGhbC0ttSAshRs5BjzE2d87+HvxoQCAKBGBY6SLBaPgThETDsNOgTEfoSTnHX"
    "/i/sPDru+ziOC5/jOOedR1tAbD0ztX/5c1cvIyvXkLwagVdI1gbwJhDrAK0OWdaEkf3BUsd0Pp0r"
    "pip51tdYfK8le4zAQYkPE7of5CEZhgj0k9i7Ni7f01Nmq45Ipe/dOS58juPURQA/Xw1nhUNHWHnL"
    "LS0nm48sqSiuDQjPkelKAotELQO4jNDlAi8jMB9QRYX/lkN4QrSTAA9DPErymGiPQTgahEcR8p2n"
    "svBI87FFj/f39p4856erVrPyc3kY03HhcxxnWgjoAnGoShw/TqzutTGTRbYg4PPVgOPH2bF6gENP"
    "DY3Mz8WHF1tva6twe4+d7Vk+jS5E7OksqjK1tsrFznFc+BynUeacpmkeu8A5juM4juM4juM4juM4"
    "juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4"
    "juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4"
    "juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM4juM0JvQmmPN9LW+aGdN33leO0yDCN9Fn"
    "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"
    "OI7jOI5zofz/2XMnPx4SurEAAAAASUVORK5CYII="
)

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>منوی رستوران</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&family=Playfair+Display:ital,wght@1,500;1,600&display=swap" rel="stylesheet">
<style>
  :root{
    --cream:#F3EEE3; --cream-card:#FBF8F1; --ink:#1E4C32; --ink-soft:#3E7A55;
    --wine:#1E4C32; --wine-dark:#123722; --gold:#2E6B44; --line:#d9e6dc;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--cream);color:var(--ink);font-family:'Vazirmatn',sans-serif;min-height:100vh;}
  header{position:relative;text-align:center;padding:48px 20px 28px;}
  .logo-img{width:170px;max-width:60%;height:auto;display:block;margin:0 auto 10px;}
  .admin-btn{position:absolute;top:16px;left:16px;background:var(--cream-card);border:1px solid var(--line);
    color:var(--ink-soft);font-family:'Vazirmatn',sans-serif;font-size:13px;padding:7px 14px;border-radius:20px;
    cursor:pointer;transition:all .2s;}
  .admin-btn:hover{border-color:var(--wine);color:var(--wine);}
  h1.title{font-family:'Vazirmatn',sans-serif;font-weight:800;font-size:36px;color:var(--wine);margin:0 0 6px;letter-spacing:0;}
  .subtitle{color:var(--ink-soft);font-size:19px;margin:0;font-family:'Playfair Display',serif;font-style:italic;font-weight:600;direction:ltr;letter-spacing:.3px;}
  .rule{width:120px;height:3px;background:var(--gold);margin:18px auto 0;border-radius:2px;}
  .instagram-link{display:inline-flex;align-items:center;gap:6px;margin-top:16px;color:var(--wine);font-family:'Vazirmatn',sans-serif;
    font-weight:600;font-size:14px;text-decoration:none;border-bottom:1.5px solid var(--wine);padding-bottom:2px;
    transition:opacity .2s;}
  .instagram-link:hover{opacity:.7;}
  .site-footer{max-width:760px;margin:30px auto 0;padding:20px 20px 40px;border-top:1px solid var(--line);
    display:flex;flex-direction:column;align-items:center;gap:14px;}
  .footer-row{display:inline-flex;flex-direction:row-reverse;align-items:center;gap:8px;color:var(--ink-soft);font-family:'Vazirmatn',sans-serif;
    font-size:13px;font-weight:500;text-decoration:none;transition:color .2s;}
  .footer-row:hover{color:var(--wine);}
  .tabs{display:flex;gap:10px;overflow-x:auto;padding:24px 20px 8px;max-width:760px;margin:0 auto;justify-content:center;flex-wrap:wrap;}
  .tab{font-family:'Vazirmatn',sans-serif;font-weight:600;font-size:14px;background:transparent;border:1.5px solid var(--line);
    color:var(--ink-soft);padding:8px 20px;border-radius:30px;cursor:pointer;white-space:nowrap;transition:all .2s;}
  .tab.active,.tab:hover{background:var(--wine);border-color:var(--wine);color:#fff;}
  main{max-width:760px;margin:0 auto;padding:20px 20px 80px;}
  .empty-state{text-align:center;color:var(--ink-soft);padding:60px 20px;font-size:15px;line-height:1.9;}
  .category-section{margin-bottom:38px;scroll-margin-top:20px;}
  .category-heading-row{display:flex;align-items:center;gap:12px;margin-bottom:6px;}
  .category-heading-img{width:46px;height:46px;border-radius:10px;object-fit:cover;flex-shrink:0;background:#eee6d3;}
  .category-heading{font-family:'Vazirmatn',sans-serif;font-weight:800;font-size:23px;color:var(--wine);margin:0;letter-spacing:0;}
  .category-sub-rule{width:100%;height:2px;background:var(--gold);margin:0 0 18px;border-radius:2px;}
  .products{display:flex;flex-direction:column;gap:16px;}
  .product-card{background:var(--cream-card);border:1px solid var(--line);border-radius:14px;padding:14px;transition:opacity .2s;}
  .product-card.sold-out{opacity:.5;}
  .product-card.has-desc{cursor:pointer;}
  .product-card-row{display:flex;align-items:center;gap:16px;}
  .sold-badge{display:inline-block;background:var(--ink-soft);color:#fff;font-size:11px;padding:2px 9px;border-radius:10px;margin-left:8px;white-space:nowrap;}
  .product-img{width:76px;height:76px;border-radius:10px;object-fit:cover;flex-shrink:0;background:#eee6d3;}
  .product-img.placeholder{display:flex;align-items:center;justify-content:center;color:#c9bfa8;font-size:11px;}
  .product-info{flex:1;min-width:0;}
  .product-line{display:flex;align-items:baseline;gap:8px;}
  .product-name{font-weight:700;font-size:16px;white-space:nowrap;overflow:hidden;min-width:0;flex-shrink:1;}
  .leader{flex:1;border-bottom:2px dotted var(--line);height:0;margin-bottom:5px;}
  .product-price{font-weight:700;color:var(--wine);font-size:15px;white-space:nowrap;}
  .desc-arrow{display:inline-block;margin-right:4px;color:var(--ink-soft);font-size:11px;transition:transform .25s ease;flex-shrink:0;}
  .desc-arrow.open{transform:rotate(180deg);}
  .product-desc-panel{max-height:0;overflow:hidden;transition:max-height .3s ease;}
  .product-desc-panel.open{max-height:500px;}
  .product-desc-panel-inner{padding:10px 4px 0;font-family:'Vazirmatn',sans-serif;font-size:13px;line-height:1.8;color:#111111;}
  .del-btn{background:none;border:none;color:#3E7A55;font-size:12px;cursor:pointer;padding:4px 8px;flex-shrink:0;}
  .del-btn:hover{color:var(--wine);}
  .overlay{position:fixed;inset:0;background:rgba(43,33,24,.5);display:flex;align-items:center;justify-content:center;z-index:100;padding:20px;}
  .hidden{display:none !important;}
  .modal{background:var(--cream);border-radius:16px;padding:28px;width:100%;max-width:420px;max-height:85vh;overflow-y:auto;box-shadow:0 20px 50px rgba(0,0,0,.25);}
  .modal h2{font-family:'Vazirmatn',sans-serif;font-weight:800;color:var(--wine);font-size:21px;margin:0 0 18px;}
  .field{margin-bottom:14px;}
  .field label{display:block;font-size:13px;color:var(--ink-soft);margin-bottom:6px;}
  input[type=text],input[type=password],input[type=number]{width:100%;padding:10px 12px;border-radius:8px;border:1px solid var(--line);
    background:#fff;font-family:'Vazirmatn',sans-serif;font-size:14px;color:var(--ink);}
  input:focus{outline:2px solid var(--gold);border-color:var(--gold);}
  input[type=file]{font-size:13px;}
  .btn{background:var(--wine);color:#fff;border:none;padding:10px 18px;border-radius:8px;font-family:'Vazirmatn',sans-serif;
    font-weight:600;font-size:14px;cursor:pointer;transition:background .2s;}
  .btn:hover{background:var(--wine-dark);}
  .btn.secondary{background:transparent;color:var(--ink-soft);border:1px solid var(--line);}
  .btn.secondary:hover{border-color:var(--wine);color:var(--wine);}
  .row-btns{display:flex;gap:10px;margin-top:6px;}
  .err-msg{color:var(--wine);font-size:13px;margin:-6px 0 12px;min-height:16px;}
  .close-x{position:absolute;top:14px;left:16px;background:none;border:none;font-size:20px;color:var(--ink-soft);cursor:pointer;}
  .admin-panel{max-width:420px;width:100%;}
  .cat-block{border:1px solid var(--line);border-radius:10px;padding:14px;margin-bottom:14px;background:var(--cream-card);}
  .cat-block-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;gap:8px;}
  .cat-head-left{display:flex;align-items:center;gap:10px;min-width:0;}
  .cat-thumb{width:38px;height:38px;border-radius:8px;object-fit:cover;flex-shrink:0;background:#eee6d3;}
  .cat-block-head h3{margin:0;font-size:16px;color:var(--wine);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .cat-head-btns{display:flex;gap:4px;flex-shrink:0;}
  .mini-product{display:flex;justify-content:space-between;align-items:center;font-size:13px;padding:7px 0;border-bottom:1px dashed var(--line);gap:8px;}
  .mini-product:last-child{border-bottom:none;}
  .mini-product-name{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  .mini-product-name.sold{text-decoration:line-through;color:#8fae9b;}
  .mini-btns{display:flex;gap:4px;flex-shrink:0;}
  .mini-btn{background:none;border:1px solid var(--line);color:var(--ink-soft);font-size:11px;padding:3px 9px;border-radius:12px;cursor:pointer;white-space:nowrap;}
  .mini-btn:hover{border-color:var(--wine);color:var(--wine);}
  .mini-btn.is-sold{background:var(--gold);border-color:var(--gold);color:#fff;}
  .toggle-form{background:none;border:1px dashed var(--gold);color:var(--gold);font-size:12px;padding:6px 10px;border-radius:20px;cursor:pointer;margin-top:8px;}
  .loading{text-align:center;color:var(--ink-soft);padding:60px 20px;}
</style>
</head>
<body>

<header>
  <button class="admin-btn" id="adminOpenBtn">مدیریت</button>
  <img class="logo-img" src="data:image/png;base64,__LOGO_B64_PLACEHOLDER__" alt="LOCAL">
  <p class="subtitle" id="subtitleText">Be kind with your taste</p>
  <div class="rule"></div>
  <a class="instagram-link" href="https://instagram.com/Cafe_local8" target="_blank" rel="noopener noreferrer">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="20" height="20" rx="5" stroke="var(--wine)" stroke-width="2"/>
      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" stroke="var(--wine)" stroke-width="2"/>
      <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" stroke="var(--wine)" stroke-width="2" stroke-linecap="round"/>
    </svg>
    لینک اینستاگرام
  </a>
</header>

<div class="tabs" id="tabs"></div>

<main id="mainContent">
  <div class="loading">در حال بارگذاری منو...</div>
</main>

<footer class="site-footer">
  <a class="footer-row" href="tel:09929119510">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="var(--wine)" xmlns="http://www.w3.org/2000/svg">
      <path d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.01-.24 11.36 11.36 0 0 0 3.58.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.36 11.36 0 0 0 .57 3.58 1 1 0 0 1-.25 1.01l-2.2 2.2z"/>
    </svg>
    <span dir="ltr">09929119510</span>
  </a>
  <a class="footer-row" href="https://instagram.com/Cafe_local8" target="_blank" rel="noopener noreferrer">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="20" height="20" rx="5" stroke="var(--wine)" stroke-width="2"/>
      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" stroke="var(--wine)" stroke-width="2"/>
      <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" stroke="var(--wine)" stroke-width="2" stroke-linecap="round"/>
    </svg>
    <span>Cafe_local8</span>
  </a>
</footer>

<div class="overlay hidden" id="loginOverlay">
  <div class="modal" style="position:relative;">
    <button class="close-x" data-close="loginOverlay">✕</button>
    <h2>ورود مدیر</h2>
    <div class="field"><label>رمز عبور</label>
      <input type="password" id="loginPassInput" placeholder="رمز عبور را وارد کنید"></div>
    <div class="err-msg" id="loginErr"></div>
    <div class="row-btns"><button class="btn" id="loginSubmitBtn">ورود</button></div>
  </div>
</div>

<div class="overlay hidden" id="setPassOverlay">
  <div class="modal" style="position:relative;">
    <button class="close-x" data-close="setPassOverlay">✕</button>
    <h2>تعیین رمز مدیریت</h2>
    <p style="font-size:13px;color:var(--ink-soft);margin-top:-8px;">
      این اولین بار است که وارد بخش مدیریت می‌شوید. یک رمز عبور انتخاب کنید؛ از این پس فقط با همین رمز می‌توانید وارد شوید.
    </p>
    <div class="field"><label>رمز عبور جدید</label>
      <input type="password" id="newPassInput" placeholder="یک رمز انتخاب کنید"></div>
    <div class="field"><label>تکرار رمز عبور</label>
      <input type="password" id="newPassConfirm" placeholder="رمز را دوباره وارد کنید"></div>
    <div class="err-msg" id="setPassErr"></div>
    <div class="row-btns"><button class="btn" id="setPassSubmitBtn">ثبت رمز و ورود</button></div>
  </div>
</div>

<div class="overlay hidden" id="adminOverlay">
  <div class="modal admin-panel" style="position:relative;">
    <button class="close-x" data-close="adminOverlay">✕</button>
    <h2>پنل مدیریت منو</h2>

    <div class="field">
      <label>متن زیر لوگو (انگلیسی)</label>
      <input type="text" id="taglineInput" placeholder="Be kind with your taste">
    </div>
    <div class="row-btns" style="margin-bottom:18px;">
      <button class="btn" id="saveTaglineBtn">ذخیره متن</button>
    </div>

    <div class="field">
      <label>افزودن سرفصل جدید (مثلاً: کیک‌ها، نوشیدنی‌ها)</label>
      <input type="text" id="newCatInput" placeholder="نام سرفصل">
    </div>
    <div class="field">
      <label>عکس سرفصل (اختیاری)</label>
      <input type="file" id="newCatImageInput" accept="image/*">
    </div>
    <div class="row-btns" style="margin-bottom:6px;">
      <button class="btn" id="addCatBtn">افزودن سرفصل</button>
    </div>
    <div id="adminCatList" style="margin-top:20px;"></div>
    <div class="row-btns" style="margin-top:10px;border-top:1px solid var(--line);padding-top:16px;">
      <button class="btn secondary" id="logoutBtn">خروج از مدیریت</button>
    </div>
  </div>
</div>

<script>
(function(){
  let menuData = { categories: [] };
  let isAdmin = false;

  const $ = id => document.getElementById(id);
  function openOverlay(id){ $(id).classList.remove('hidden'); }
  function closeOverlay(id){ $(id).classList.add('hidden'); }
  document.querySelectorAll('[data-close]').forEach(btn=>{
    btn.addEventListener('click', ()=> closeOverlay(btn.dataset.close));
  });

  // ---------- ارتباط با بک‌اند پایتون ----------
  async function loadMenu(){
    const res = await fetch('/api/menu');
    menuData = await res.json();
  }
  async function saveMenu(){
    await fetch('/api/menu', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(menuData)
    });
  }
  async function passwordExists(){
    const res = await fetch('/api/password/status');
    const d = await res.json();
    return d.exists;
  }
  async function setPassword(pass){
    const res = await fetch('/api/password/set', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({password: pass})
    });
    return res.ok;
  }
  async function verifyPassword(pass){
    const res = await fetch('/api/password/verify', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({password: pass})
    });
    const d = await res.json();
    return d.ok;
  }
  async function loadTagline(){
    try{
      const res = await fetch('/api/tagline');
      const d = await res.json();
      if(d.tagline){ $('subtitleText').textContent = d.tagline; }
    } catch(e){ /* ignore, keep default text */ }
  }
  async function saveTagline(text){
    const res = await fetch('/api/tagline', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({tagline: text})
    });
    return res.ok;
  }

  function uid(){ return Date.now().toString(36) + Math.random().toString(36).slice(2,7); }

  function formatPrice(p){
    if(p === '' || p === undefined || p === null) return '';
    const n = Number(String(p).replace(/[^0-9.]/g,''));
    if(isNaN(n) || String(p).trim()===''){ return p; }
    return n.toLocaleString('en-US') + ' تومان';
  }

  function renderTabs(){
    const tabsEl = $('tabs');
    tabsEl.innerHTML = '';
    const nonEmptyCats = menuData.categories.filter(c => c.products.length > 0);
    if(nonEmptyCats.length < 2) return; // با صفر یا یک سرفصل، نیازی به تب پرش نیست
    nonEmptyCats.forEach(cat=>{
      const b = document.createElement('button');
      b.className = 'tab';
      b.textContent = cat.name;
      b.addEventListener('click', ()=>{
        const section = document.getElementById('cat-section-' + cat.id);
        if(section) section.scrollIntoView({ behavior:'smooth', block:'start' });
      });
      tabsEl.appendChild(b);
    });
  }

  function renderProducts(){
    const main = $('mainContent');
    main.innerHTML = '';

    if(menuData.categories.length === 0){
      main.innerHTML = '<div class="empty-state">منو هنوز خالی است.<br>برای افزودن سرفصل و محصولات، از دکمه «مدیریت» بالای صفحه استفاده کنید.</div>';
      return;
    }

    const nonEmptyCats = menuData.categories.filter(c => c.products.length > 0);
    if(nonEmptyCats.length === 0){
      main.innerHTML = '<div class="empty-state">هنوز محصولی ثبت نشده است.</div>';
      return;
    }

    nonEmptyCats.forEach(cat=>{
      const section = document.createElement('div');
      section.className = 'category-section';
      section.id = 'cat-section-' + cat.id;

      const headRow = document.createElement('div');
      headRow.className = 'category-heading-row';
      if(cat.image){
        const img = document.createElement('img');
        img.className = 'category-heading-img';
        img.src = cat.image;
        img.alt = cat.name;
        headRow.appendChild(img);
      }
      const heading = document.createElement('h2');
      heading.className = 'category-heading';
      heading.textContent = cat.name;
      headRow.appendChild(heading);
      section.appendChild(headRow);

      const subRule = document.createElement('div');
      subRule.className = 'category-sub-rule';
      section.appendChild(subRule);

      const wrap = document.createElement('div');
      wrap.className = 'products';
      cat.products.forEach(p=>{
        const hasDesc = !!(p.desc && p.desc.trim());
        const card = document.createElement('div');
        card.className = 'product-card' + (p.soldOut ? ' sold-out' : '') + (hasDesc ? ' has-desc' : '');
        card.innerHTML = `
          <div class="product-card-row">
            ${p.image ? `<img class="product-img" src="${p.image}" alt="${p.name}">` : `<div class="product-img placeholder">بدون عکس</div>`}
            <div class="product-info">
              <div class="product-line">
                <span class="product-name">${escapeHtml(p.name)}</span>
                <span class="leader"></span>
                ${p.soldOut ? `<span class="sold-badge">تمام شده</span>` : ''}
                ${hasDesc ? `<span class="desc-arrow">▾</span>` : ''}
                <span class="product-price">${formatPrice(p.price)}</span>
              </div>
            </div>
          </div>
          ${hasDesc ? `
          <div class="product-desc-panel">
            <div class="product-desc-panel-inner">${escapeHtml(p.desc)}</div>
          </div>` : ''}`;

        if(hasDesc){
          const row = card.querySelector('.product-card-row');
          const panel = card.querySelector('.product-desc-panel');
          const arrow = card.querySelector('.desc-arrow');
          row.addEventListener('click', ()=>{
            const isOpen = panel.classList.toggle('open');
            arrow.classList.toggle('open', isOpen);
          });
        }

        wrap.appendChild(card);
      });
      section.appendChild(wrap);

      main.appendChild(section);
    });

    fitLongProductNames();
  }

  // اگر اسم محصول طولانی بود، فونتش رو خودکار کوچیک می‌کنیم تا از قاب بیرون نزنه
  function fitLongProductNames(){
    const MAX_FONT = 16, MIN_FONT = 10, STEP = 0.5;
    document.querySelectorAll('.product-name').forEach(el=>{
      el.style.fontSize = MAX_FONT + 'px';
      let fontSize = MAX_FONT;
      while(fontSize > MIN_FONT && el.scrollWidth > el.clientWidth){
        fontSize -= STEP;
        el.style.fontSize = fontSize + 'px';
      }
    });
  }

  let fitNamesResizeTimer = null;
  window.addEventListener('resize', ()=>{
    clearTimeout(fitNamesResizeTimer);
    fitNamesResizeTimer = setTimeout(fitLongProductNames, 150);
  });

  function escapeHtml(str){
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  function escapeAttr(str){
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  async function populateTaglineInput(){
    try{
      const res = await fetch('/api/tagline');
      const d = await res.json();
      $('taglineInput').value = d.tagline || '';
    } catch(e){ $('taglineInput').value = ''; }
  }

  $('adminOpenBtn').addEventListener('click', async ()=>{
    if(isAdmin){ renderAdminPanel(); populateTaglineInput(); openOverlay('adminOverlay'); return; }
    const exists = await passwordExists();
    if(!exists){
      $('newPassInput').value=''; $('newPassConfirm').value=''; $('setPassErr').textContent='';
      openOverlay('setPassOverlay');
    } else {
      $('loginPassInput').value=''; $('loginErr').textContent='';
      openOverlay('loginOverlay');
    }
  });

  $('setPassSubmitBtn').addEventListener('click', async ()=>{
    const p1 = $('newPassInput').value;
    const p2 = $('newPassConfirm').value;
    if(!p1 || p1.length < 4){ $('setPassErr').textContent = 'رمز باید حداقل ۴ کاراکتر باشد.'; return; }
    if(p1 !== p2){ $('setPassErr').textContent = 'رمزها یکسان نیستند.'; return; }
    const ok = await setPassword(p1);
    if(!ok){ $('setPassErr').textContent = 'خطا در ثبت رمز.'; return; }
    isAdmin = true;
    closeOverlay('setPassOverlay');
    renderAdminPanel();
    populateTaglineInput();
    openOverlay('adminOverlay');
  });

  $('loginSubmitBtn').addEventListener('click', async ()=>{
    const entered = $('loginPassInput').value;
    const ok = await verifyPassword(entered);
    if(ok){
      isAdmin = true;
      closeOverlay('loginOverlay');
      renderAdminPanel();
      populateTaglineInput();
      openOverlay('adminOverlay');
    } else {
      $('loginErr').textContent = 'رمز عبور اشتباه است.';
    }
  });

  $('loginPassInput').addEventListener('keydown', e=>{ if(e.key==='Enter') $('loginSubmitBtn').click(); });
  $('newPassConfirm').addEventListener('keydown', e=>{ if(e.key==='Enter') $('setPassSubmitBtn').click(); });

  $('logoutBtn').addEventListener('click', ()=>{
    isAdmin = false;
    closeOverlay('adminOverlay');
  });

  $('saveTaglineBtn').addEventListener('click', async ()=>{
    const text = $('taglineInput').value.trim();
    if(!text){ alert('متن نمی‌تواند خالی باشد.'); return; }
    const ok = await saveTagline(text);
    if(ok){
      $('subtitleText').textContent = text;
      alert('متن با موفقیت ذخیره شد.');
    } else {
      alert('خطا در ذخیره‌سازی.');
    }
  });

  $('addCatBtn').addEventListener('click', async ()=>{
    const input = $('newCatInput');
    const imageInput = $('newCatImageInput');
    const name = input.value.trim();
    if(!name) return;

    let imageData = null;
    if(imageInput.files && imageInput.files[0]){
      try{ imageData = await resizeImageToDataURL(imageInput.files[0], 300); }
      catch(e){ alert('خطا در پردازش تصویر سرفصل. سرفصل بدون عکس ذخیره می‌شود.'); }
    }

    menuData.categories.push({ id: uid(), name, image: imageData, products: [] });
    input.value = '';
    imageInput.value = '';
    await saveMenu();
    renderAdminPanel(); renderTabs(); renderProducts();
  });

  function renderAdminPanel(){
    const listEl = $('adminCatList');
    listEl.innerHTML = '';
    if(menuData.categories.length === 0){
      listEl.innerHTML = '<p style="font-size:13px;color:var(--ink-soft);">هنوز سرفصلی ثبت نشده. یکی اضافه کنید.</p>';
      return;
    }
    menuData.categories.forEach(cat=>{
      const block = document.createElement('div');
      block.className = 'cat-block';

      // ---- سربرگ سرفصل ----
      const head = document.createElement('div');
      head.className = 'cat-block-head';

      const headLeft = document.createElement('div');
      headLeft.className = 'cat-head-left';
      if(cat.image){
        const thumb = document.createElement('img');
        thumb.className = 'cat-thumb';
        thumb.src = cat.image;
        headLeft.appendChild(thumb);
      }
      const h3 = document.createElement('h3');
      h3.textContent = cat.name;
      headLeft.appendChild(h3);
      head.appendChild(headLeft);

      const headBtns = document.createElement('div');
      headBtns.className = 'cat-head-btns';
      const editCatBtn = document.createElement('button');
      editCatBtn.className = 'mini-btn';
      editCatBtn.textContent = 'ویرایش';
      const delCatBtn = document.createElement('button');
      delCatBtn.className = 'del-btn';
      delCatBtn.textContent = 'حذف';
      delCatBtn.addEventListener('click', async ()=>{
        if(!confirm(`سرفصل «${cat.name}» و همه محصولات آن حذف شود؟`)) return;
        menuData.categories = menuData.categories.filter(c=>c.id!==cat.id);
        await saveMenu();
        renderAdminPanel(); renderTabs(); renderProducts();
      });
      headBtns.appendChild(editCatBtn);
      headBtns.appendChild(delCatBtn);
      head.appendChild(headBtns);
      block.appendChild(head);

      // ---- فرم ویرایش سرفصل (نام و عکس) ----
      const catEditForm = document.createElement('div');
      catEditForm.className = 'hidden';
      catEditForm.style.marginBottom = '12px';
      catEditForm.innerHTML = `
        <div class="field"><label>نام سرفصل</label><input type="text" class="cf-name" value="${escapeAttr(cat.name)}"></div>
        <div class="field"><label>عکس جدید سرفصل (اختیاری - در صورت انتخاب، عکس قبلی جایگزین می‌شود)</label><input type="file" class="cf-image" accept="image/*"></div>
        <div class="row-btns">
          <button class="btn cf-save">ذخیره</button>
          <button class="btn secondary cf-cancel">انصراف</button>
        </div>`;
      block.appendChild(catEditForm);

      editCatBtn.addEventListener('click', ()=>{ catEditForm.classList.toggle('hidden'); });
      catEditForm.querySelector('.cf-cancel').addEventListener('click', ()=> catEditForm.classList.add('hidden'));
      catEditForm.querySelector('.cf-save').addEventListener('click', async ()=>{
        const newName = catEditForm.querySelector('.cf-name').value.trim();
        const fileInput = catEditForm.querySelector('.cf-image');
        if(!newName){ alert('نام سرفصل نمی‌تواند خالی باشد.'); return; }
        cat.name = newName;
        if(fileInput.files && fileInput.files[0]){
          try{ cat.image = await resizeImageToDataURL(fileInput.files[0], 300); }
          catch(e){ alert('خطا در پردازش تصویر جدید.'); }
        }
        await saveMenu();
        renderAdminPanel(); renderTabs(); renderProducts();
      });

      // ---- لیست محصولات ----
      const prodListEl = document.createElement('div');
      cat.products.forEach(p=>{
        const row = document.createElement('div');
        row.className = 'mini-product';

        const nameSpan = document.createElement('span');
        nameSpan.className = 'mini-product-name' + (p.soldOut ? ' sold' : '');
        nameSpan.textContent = `${p.name} — ${formatPrice(p.price)}`;
        row.appendChild(nameSpan);

        const btnsWrap = document.createElement('div');
        btnsWrap.className = 'mini-btns';

        const soldBtn = document.createElement('button');
        soldBtn.className = 'mini-btn' + (p.soldOut ? ' is-sold' : '');
        soldBtn.textContent = p.soldOut ? 'موجود شد' : 'تمام شد';
        soldBtn.addEventListener('click', async ()=>{
          p.soldOut = !p.soldOut;
          await saveMenu();
          renderAdminPanel(); renderTabs(); renderProducts();
        });

        const editBtn = document.createElement('button');
        editBtn.className = 'mini-btn';
        editBtn.textContent = 'ویرایش';

        const delBtn = document.createElement('button');
        delBtn.className = 'del-btn';
        delBtn.textContent = 'حذف';
        delBtn.addEventListener('click', async ()=>{
          if(!confirm(`محصول «${p.name}» حذف شود؟`)) return;
          cat.products = cat.products.filter(x=>x.id!==p.id);
          await saveMenu();
          renderAdminPanel(); renderTabs(); renderProducts();
        });

        btnsWrap.appendChild(soldBtn);
        btnsWrap.appendChild(editBtn);
        btnsWrap.appendChild(delBtn);
        row.appendChild(btnsWrap);
        prodListEl.appendChild(row);

        // ---- فرم ویرایش محصول ----
        const editForm = document.createElement('div');
        editForm.className = 'hidden';
        editForm.style.margin = '4px 0 12px';
        editForm.innerHTML = `
          <div class="field"><label>نام محصول</label><input type="text" class="ef-name" value="${escapeAttr(p.name)}"></div>
          <div class="field"><label>قیمت (تومان)</label><input type="text" class="ef-price" value="${escapeAttr(p.price || '')}"></div>
          <div class="field"><label>توضیح کوتاه (اختیاری)</label><input type="text" class="ef-desc" value="${escapeAttr(p.desc || '')}"></div>
          <div class="field"><label>عکس جدید محصول (اختیاری - در صورت انتخاب جایگزین می‌شود)</label><input type="file" class="ef-image" accept="image/*"></div>
          <div class="row-btns">
            <button class="btn ef-save">ذخیره تغییرات</button>
            <button class="btn secondary ef-cancel">انصراف</button>
          </div>`;
        prodListEl.appendChild(editForm);

        editBtn.addEventListener('click', ()=>{ editForm.classList.toggle('hidden'); });
        editForm.querySelector('.ef-cancel').addEventListener('click', ()=> editForm.classList.add('hidden'));
        editForm.querySelector('.ef-save').addEventListener('click', async ()=>{
          const newName = editForm.querySelector('.ef-name').value.trim();
          const newPrice = editForm.querySelector('.ef-price').value.trim();
          const newDesc = editForm.querySelector('.ef-desc').value.trim();
          const fileInput = editForm.querySelector('.ef-image');
          if(!newName){ alert('نام محصول نمی‌تواند خالی باشد.'); return; }

          p.name = newName;
          p.price = newPrice;
          p.desc = newDesc;
          if(fileInput.files && fileInput.files[0]){
            try{ p.image = await resizeImageToDataURL(fileInput.files[0], 400); }
            catch(e){ alert('خطا در پردازش تصویر جدید.'); }
          }
          await saveMenu();
          renderAdminPanel(); renderTabs(); renderProducts();
        });
      });
      block.appendChild(prodListEl);

      const toggleBtn = document.createElement('button');
      toggleBtn.className = 'toggle-form';
      toggleBtn.textContent = '+ افزودن محصول به این سرفصل';
      block.appendChild(toggleBtn);

      const formEl = document.createElement('div');
      formEl.className = 'hidden';
      formEl.style.marginTop = '12px';
      formEl.innerHTML = `
        <div class="field"><label>نام محصول</label><input type="text" class="pf-name" placeholder="مثلاً کیک شکلاتی"></div>
        <div class="field"><label>قیمت (تومان)</label><input type="text" class="pf-price" placeholder="مثلاً 250000"></div>
        <div class="field"><label>توضیح کوتاه (اختیاری)</label><input type="text" class="pf-desc" placeholder="مثلاً با گاناش شکلاتی"></div>
        <div class="field"><label>عکس محصول (اختیاری)</label><input type="file" class="pf-image" accept="image/*"></div>
        <div class="row-btns"><button class="btn pf-submit">ذخیره محصول</button></div>`;
      block.appendChild(formEl);

      toggleBtn.addEventListener('click', ()=>{ formEl.classList.toggle('hidden'); });

      formEl.querySelector('.pf-submit').addEventListener('click', async ()=>{
        const nameInput = formEl.querySelector('.pf-name');
        const priceInput = formEl.querySelector('.pf-price');
        const descInput = formEl.querySelector('.pf-desc');
        const fileInput = formEl.querySelector('.pf-image');
        const name = nameInput.value.trim();
        const price = priceInput.value.trim();
        const desc = descInput.value.trim();
        if(!name){ alert('نام محصول را وارد کنید.'); return; }

        let imageData = null;
        if(fileInput.files && fileInput.files[0]){
          try{ imageData = await resizeImageToDataURL(fileInput.files[0], 400); }
          catch(e){ alert('خطا در پردازش تصویر. محصول بدون عکس ذخیره می‌شود.'); }
        }
        cat.products.push({ id: uid(), name, price, desc, image: imageData, soldOut: false });
        await saveMenu();
        renderAdminPanel(); renderTabs(); renderProducts();
      });

      listEl.appendChild(block);
    });
  }


  function resizeImageToDataURL(file, maxWidth){
    return new Promise((resolve, reject)=>{
      const reader = new FileReader();
      reader.onload = (e)=>{
        const img = new Image();
        img.onload = ()=>{
          let w = img.width, h = img.height;
          if(w > maxWidth){ h = Math.round(h * (maxWidth / w)); w = maxWidth; }
          const canvas = document.createElement('canvas');
          canvas.width = w; canvas.height = h;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, w, h);
          resolve(canvas.toDataURL('image/jpeg', 0.82));
        };
        img.onerror = reject;
        img.src = e.target.result;
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  (async function init(){
    await loadMenu();
    await loadTagline();
    renderTabs();
    renderProducts();
  })();
})();
</script>
</body>
</html>
"""

HTML_PAGE = HTML_PAGE.replace("__LOGO_B64_PLACEHOLDER__", LOGO_B64)


if __name__ == "__main__":
    # روی همه‌ی آدرس‌های شبکه گوش می‌ده تا از مرورگر همون گوشی هم قابل دسترسی باشه
    app.run(host="0.0.0.0", port=5000, debug=False)
