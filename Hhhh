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
    "rg8gFQKfrwAAAABJRU5ErkJggg=="
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
  .logo-img{width:260px;max-width:80%;height:auto;display:block;margin:0 auto 10px;}
  .admin-btn{position:absolute;top:16px;left:16px;background:var(--cream-card);border:1px solid var(--line);
    color:var(--ink-soft);font-family:'Vazirmatn',sans-serif;font-size:13px;padding:7px 14px;border-radius:20px;
    cursor:pointer;transition:all .2s;}
  .admin-btn:hover{border-color:var(--wine);color:var(--wine);}
  h1.title{font-family:'Vazirmatn',sans-serif;font-weight:800;font-size:36px;color:var(--wine);margin:0 0 6px;letter-spacing:0;}
  .subtitle{color:var(--ink-soft);font-size:19px;margin:0;font-family:'Playfair Display',serif;font-style:italic;font-weight:600;direction:ltr;letter-spacing:.3px;}
  .rule{width:120px;height:3px;background:var(--gold);margin:18px auto 0;border-radius:2px;}
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
  .product-card-row{display:flex;align-items:center;gap:16px;direction:ltr;}
  .sold-badge{display:inline-block;background:var(--ink-soft);color:#fff;font-size:11px;padding:2px 9px;border-radius:10px;margin-left:8px;white-space:nowrap;}
  .product-img{width:76px;height:76px;border-radius:10px;object-fit:cover;flex-shrink:0;background:#eee6d3;}
  .product-img.placeholder{display:flex;align-items:center;justify-content:center;color:#c9bfa8;font-size:11px;}
  .product-info{flex:1;min-width:0;}
  .product-line{display:flex;align-items:baseline;gap:8px;}
  .product-name{font-weight:700;font-size:16px;white-space:nowrap;}
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
</header>

<div class="tabs" id="tabs"></div>

<main id="mainContent">
  <div class="loading">در حال بارگذاری منو...</div>
</main>

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
  }

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
          renderAdminPanel(); renderProducts();
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
          renderAdminPanel(); renderProducts();
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
          renderAdminPanel(); renderProducts();
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
        renderAdminPanel(); renderProducts();
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
