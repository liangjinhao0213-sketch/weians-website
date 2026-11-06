# Weinas · 铝门窗外贸独立站首页

依据《Weinas 铝门窗外贸独立站-首页设计提示词》实现的**可直接上线的静态首页**（纯 HTML / CSS / JS，无框架、无构建、无外部 CDN 依赖）。

---

## 1. 快速预览

- **最省事**：双击 `start-site.bat`（或直接双击 `index.html`）——字体、图片、脚本全部本地化，`file://` 下已验证可用，断网也能看。
- **最接近线上**：双击 `start-server.bat`，会自动用 Python 起一个本地服务并打开 http://127.0.0.1:8080/（没装 Python 时会自动退回直接打开文件）。想在局域网给同事看，用 `python -m http.server 8080 --bind 0.0.0.0` 再用本机 IP 访问。
- 命令行方式：`python -m http.server 8080`

`_source/previews/` 内有两张验收截图：`home-hero-desktop.jpg`（首屏 1440×900）与 `home-footer-desktop.jpg`（页脚 1440）。

建议浏览顺序：首屏 → 12 个品类 → Top Picks（含型材截面剖切图）→ Indoor/Outdoor → 工厂实力 → 认证 → 工程案例 → B2B 目录（悬停显示参数与询盘）→ Featured Collections（切换 By opening / By application）→ 询盘表单 → 页脚。

---

## 2. 文件结构

```
index.html                 首页（全部文案在此，可直接改）
start-site.bat             双击：用默认浏览器打开首页（离线可用）
start-server.bat           双击：起本地 http 服务 http://127.0.0.1:8080/
blog/index.html            Journal 列表（首页 08 Journal 区块指向这里）
blog/<slug>.html           6 篇文章详情页
robots.txt / sitemap.xml   SEO 基础文件（域名请替换为正式域名）
blog/                     Journal: index.html + 6 article pages
about-us/                 Company profile, factory tour, quality control
assets/
  css/style.css            设计系统 + 全部版式（约 1,600 行，含响应式）
  css/fonts.css            自托管 Inter 变量字体声明
  fonts/                   Inter woff2（latin / latin-ext 子集）
  js/main.js               交互脚本（无依赖，约 430 行）
  img/
    logo.png               公司现有品牌 logo（透明底 830×228，用于白底页眉）
    logo-on-dark.png       深底反白版（同上尺寸，页脚/分享图用；由原图程序化派生）
    favicon.png            站点图标 64×64（白底 + logo）
    apple-touch-icon.png   iOS 主屏图标 180×180
    og-image.jpg           社媒分享图 1200×630（logo + 标题）
    hero-villa-*.jpg       首屏图（1600 / 2400 / 移动端专用）
    lifestyle-dusk-*.jpg   室内外联通横幅
    top-pick-frames.jpg    Top Picks 主图
    project-*.jpg          工程案例 6 张
    factory-*.jpg          工厂纪实 4 张（其中 factory-sign.jpg 为客户实拍厂房+装柜图，2x 增强版）
    collection-*.jpg       场景集合 5 张
    ws90-section.svg       型材截面剖切详图（自绘）
    products/*.svg         12 个品类的技术立面图（自绘，统一线宽与比例）
_source/                   生成与校验脚本 + 原始 logo（可保留，也可删除，不影响前台）
    logo-original.png      客户提供的 logo 原始文件（未裁切，留档）
```

---

## 3. 已实现的内容（对照提示词）

| 提示词要求 | 实现情况 |
|---|---|
| 页眉：logo 原图 / 12 项 Products 下拉 / 搜索 / Get A Quote / 半透明毛玻璃 / 72–80px | ✅ 固定页眉 76px，滚动后 66px + 模糊加深；下拉为双列 12 项，顺序与文案逐字一致 |
| 主菜单：Home·Products▾·Videos·About Us·Contact Us·News·Cases | ✅ 顺序、拼写完全一致（Videos / News 为预留内页） |
| Hero：全幅建筑实景 + 标题 + 副标题 + CTA | ✅ 深色铝板别墅暮色实景；标题 "Engineered Aluminium Openings for Modern Architecture" |
| 分类入口：三列 12 品类 + 一行参数 | ✅ 三列为 1px 发丝线网格；每项含编号、技术立面图、参数行 |
| Top Picks：大图 + 型材截面 + 关键性能数字 | ✅ WS-90 实景 + 自绘 Section A–A 剖切详图（含 22 mm 视线的尺寸标注）+ 5 项指标条 |
| Lifestyle Banner | ✅ 暮色室内外联通大图 + 白色杂志式文字卡 |
| 工厂实力条：实拍 + 数字证明 | ✅ 2×2 纪实图 + 6 步工艺流程 + 四组数字（15+ / 40,000 m² / 60+ / 7 天） |
| 认证信任行（单色） | ✅ 浅灰底 6 格，ISO 9001 / CE / SGS / AS 2047 / NFRC / Uw Test，另附说明行 |
| Project Cases 编辑式瀑布墙 | ✅ CSS 多列瀑布流（3/2/1 列自适应），地点 + 类型 + 系统说明 |
| Shop 预览：统一白底、B2B 不显示价格、hover 出参数 + Request A Quote | ✅ 1:1 图框，hover 上滑显示 3 行参数与询盘按钮；标注 “B2B only — pricing on request” |
| Featured Collection：按开启方式 / 应用场景横向滚动 | ✅ 双 Tab 切换（技术图 / 场景图两组），支持拖拽、箭头、键盘、滚动吸附 |
| 页脚：深蓝 + 产品地图 + 地址 + WhatsApp/邮箱/电话 + 订阅 + 悬浮 CTA | ✅ 四栏页脚 + 品牌行 “Weinas Window & Door Co., Ltd. — Doors And Windows Manufacturer”，右下角常驻悬浮询盘按钮 |
| 配色、字体、发丝线、无阴影/无渐变/2px 圆角 | ✅ 全套 CSS 变量：`#0B2B5B / #C7CCD2 / #2B2F33 / #E8E9EB / #F6F7F8`，古铜仅用于热桥标记 |
| TDK + 品牌一致性 | ✅ Title/Description/OG/Twitter/JSON-LD Organization；全站文案只用 Weinas |

**交互细节**：滚动毛玻璃页眉、滚动高亮当前栏目、Products 下拉（悬停 / 点击 / Esc / 键盘可达）、全屏搜索（输入即筛选 12 品类，“/” 快捷键，Esc 关闭）、移动端全屏菜单 + 产品手风琴、Tab 切换、横滑拖拽与箭头联动、进场渐显（尊重 `prefers-reduced-motion`）、表单本地校验与提交反馈、文件选择文件名回显、页脚年份自动更新。

---

## 4. 需要注意 / 替换的内容

1. **联系方式与地址已替换为真实信息**：电话 / WhatsApp `+86 178 1881 9386`、邮箱 `liangjinhao0213@gmail.com`、地址 `No. 7, Dalingdi, Zhongxiu Second Village Group, Tangbian Village, Shishan Town, Foshan, Guangdong, China`（页脚、询盘区、移动端菜单、`tel:` / `wa.me` 链接、JSON-LD 结构化数据均已同步）。
   - 仍待确认的只有**网站域名**：`canonical`、`og:url`、JSON-LD、`robots.txt`、`sitemap.xml` 里暂时写的是 `www.weinas.com`，域名定了之后全局替换即可。
   - 建议：B2B 询盘用企业域名邮箱（如 `sales@weinas.com`）比 gmail 更可信；若开通，全局替换 `liangjinhao0213@gmail.com` 即可（共 5 处）。
2. **表单没有后端**：`#quote-form` 提交后仅做前端校验并显示成功提示。接入方式：把 `main.js` 中 `fakeSubmit()` 的 `e.preventDefault()` 分支改成 `fetch('/api/inquiry', ...)`，或直接给 `<form action="..." method="post">` 并删除 JS 拦截。
3. **图片为版权友好的建筑/工业实拍素材（Unsplash License，可商用免署名）**，用于版式验证；正式上线建议全部替换为**自有工厂与工程实拍**（提示词也明确要求不要图库假图）。替换时保持同名同比例即可，无需改代码；建议 Hero 2400×1180、案例 4:5 或 16:10、工厂 4:3。
4. **产品图为自绘技术立面图**，替代“白底去背产品摄影”——统一线宽、统一比例、可无限清晰缩放，且规避了“3D 渲染假产品”“伪造认证”等负向要求。拿到真实产品摄影后，把 `assets/img/products/*.svg` 换成同名 `.jpg/.png` 并修改 `index.html` 中对应 `src` 即可。
5. **案例地点与项目名为示例**（Palm Beach / Shibuya / Al Quoz 等），请换成真实项目，避免对外传播时产生事实性误导。
6. **内页未包含**：`/videos/`、`/news/`、`/cases/`、`/downloads/*.pdf`、`/privacy/` 等链接带 `data-coming-soon`，点击会弹出说明提示而不是 404。做好内页后删除该属性即可。
7. **性能**：首屏图已预加载并区分移动端；其余图片 `loading="lazy"`；字体自托管（无需 Google Fonts，中国大陆与海外均不受阻）。
8. **Logo 使用方式（两套）**：
   - 页眉（白底）：`logo.png` 原图，等高 46px（滚动后 38px；移动端 40/34px）。
   - 页脚（深蓝底 / 分享图）：`logo-on-dark.png` 反白版，宽 190px。原 logo 的蓝（≈`#0A4885`）放在 `#0B2B5B` 上会糊掉，白底板又显得像贴纸，因此做了“深底反白”处理——**保留原图的 3D 明暗与字形，只把蓝色系映射为浅银白**，字标（WEINAS）亮、副标（Doors And Windows Manufacturer）压暗一档形成主次。生成脚本：`_source/logo_dark_variants.py`（可重跑，也保留了 A/B/C/G 等备选版本于 `_source/logo-variants/`）。
   - 若后续拿到官方“深底反白版”文件，直接覆盖 `assets/img/logo-on-dark.png` 即可，页面无需改动。
9. **Logo 替换**：直接覆盖 `assets/img/logo.png` 即可（保持透明底；建议高度 ≥ 200px）。若更换比例，需同步调整 `index.html` 中两处 `width/height` 属性（页眉 167×46、页脚 168×46）与 `.brand img` 的 `height`。
10. **配色提示**：站点主色沿用设计提示词指定的 `#0B2B5B`；logo 里的蓝约为 `#0A4885`、金属灰约为 `#8D8D8D`。若希望页眉按钮等强调色与 logo 蓝完全一致，把 `style.css` 里的 `--navy` 改为 `#0A4885` 即可（其余颜色都由变量派生，无需逐处修改）。

---

## 5. 改动指引

- **改文案**：全部在 `index.html`；12 个品类的名称、参数、链接在多处复用（页眉下拉、分类网格、页脚、搜索），建议全局搜索品类英文名后统一替换。
- **改颜色 / 字号 / 间距**：`assets/css/style.css` 顶部 `:root` 变量（`--navy`、`--fs-h1`、`--gutter` 等），其余样式全部引用变量。
- **改版式骨架**：`.container`（最大 1480px）+ `.grid-12`（12 列瑞士网格）；区块统一用 `.section` 控制上下留白。
- **重新生成图片 / 图稿**：`_source/` 内脚本（需要 Python 3 + Pillow）：
  - `build_images.py`：按目标尺寸裁切、调色、生成响应式尺寸；
  - `products.py`：重新生成 12 张产品立面图与截面图（改坐标即可）；
  - `build_site.py`：由产品数据表重新拼装 `index.html`（⚠️ 会覆盖手改内容，后期直接改 HTML 更稳妥）；
  - `shot.mjs` / `audit.mjs`：基于 CDP 的分屏截图与控制台/资源审计（需本地 Chrome/Edge）。

---

## 6. 验收自查

- 断点：1440 / 1280 / 1024 / 834 / 390 已逐屏截图检查；`1440×900` 首屏完整呈现标题、副标题、双 CTA 与数据条。
- 功能冒烟测试（CDP 自动化）：Products 下拉开合、搜索 “/” 唤起与 Esc 关闭、搜索过滤、Tab 切换与箭头启用状态、双 Rail 独立滚动、产品悬停参数层、文件选择文件名回显、表单必填校验与提交反馈、Toast 提示、悬浮 CTA 显隐——全部通过。
- 语义与可达性：单一 `h1`、跳转到正文链接、`aria-expanded` / `aria-selected` / `aria-controls`、焦点可见样式、`sr-only` 标签、`prefers-reduced-motion` 降级、图片均带 `alt`。
- 控制台：无 JS 异常、无资源加载失败（46 张图片全部加载成功）。
- 颜色对比：正文 `#6E757C` 于白底 ≈ 4.9:1；导航与按钮均达 AA。

---

## 7. 本地阶段 vs 上线阶段

目前是**纯静态本地站点**：不需要域名、不需要服务器、不需要数据库，拷到任何电脑（含 U 盘）都能打开。

### 现在就能做的（本地）

- 双击 `start-site.bat` 或 `start-server.bat` 自查看效果；改文案直接编辑 `index.html`，刷新即生效。
- 用浏览器开发者工具（F12）切到手机尺寸（iPhone / Android 预设）看响应式效果。
- 把整个 `weinas-site` 文件夹打包发给客户/同事预览，对方无需安装任何东西。

### 本地阶段的已知限制（上线时需要处理）

| 项目 | 现状 | 上线时怎么处理 |
|---|---|---|
| 询盘表单 | 前端校验 + 成功提示，**不会真的发送**（`main.js` 里的 `fakeSubmit()`） | 接后端/表单服务（PHP、Node、Formspree 等），把 `fetch()` 指向接口；或改成 `<form action="...">` 直接提交 |
| 域名 | `canonical` / `og:url` / JSON-LD / `robots.txt` / `sitemap.xml` 里是 `www.weinas.com` | 买到域名后全局替换（已在 HTML 里留了 TODO 注释） |
| 内页 | `Videos` / `News` / `Cases` / 资料下载等为 `data-coming-soon` 占位，点击弹提示 | 内页做好后删掉该属性即可正常跳转 |
| 图片 | 建筑/工业素材为版权友好占位图 | 换成自有工厂与工程实拍（同名同比例替换，无需改代码） |
| 统计 | 无 | 上线后加 Google Analytics 4 / Clarity，或先只看 Search Console |

### 买域名 + 服务器时的清单

1. **域名**：建议 `.com`，与品牌一致（如 `weinas.com`），同时把 `.cn`、常见变体做 301 保护。
2. **主机**：纯静态站 → 静态托管最省心（Cloudflare Pages / Netlify / Vercel，免费额度够用）；若在国内放，需备案的国内主机（阿里云/腾讯云轻量）或香港/新加坡主机免备案。**本项目的目录结构可直接上传，无需构建**。
3. **HTTPS**：托管平台默认自带；自有服务器用 Let's Encrypt（宝塔/宝塔面板一键）。
4. **表单后端**：静态托管方案下推荐接 Cloudflare Workers / Formspree / 企业邮箱 SMTP 接口；有 PHP 主机就写个 `send.php`。
5. **SEO 收尾**：替换域名 → 提交 `sitemap.xml` 到 Google Search Console / Bing → 配 301（若有老站）→ 验证结构化数据。
6. **上线后自测**：手机真机走一遍询盘、WhatsApp 点击、电话点击；用 PageSpeed Insights 看 LCP/CLS。

一句话：**现在这个文件夹就是最终产物**，买好域名和服务器后，替换域名 + 接表单接口 + 换成实拍图，即可上线。

---

## 8. About / Blog 页面（内容迁移）

**About us**（页眉悬停下拉，三项）：
`about-us/company-profile.html`（点击 About Us 直接进这里）、`factory-tour.html`、`quality-control.html`。
正文事实取自公司现网（aluminium-windowsdoors.com）：**2010 年成立、10,000 m² 厂房、50–100 人、出口占 60–70%**，与首页数据一致。

**Blog**（页眉 News 已改为 Blog）：
`blog/index.html` 为列表页（1 篇置顶 + 5 篇归档），另有 6 个文章详情页。内容来自现网 news.html 的 6 篇最新文章，文字保留、版式重做（卡片式、非原来的竖向长列表）。

- 首页 **08 Journal** 区块展示最新 3 篇（按日期倒序），点击进入详情；右侧 "All articles" 进列表页。
- 文章配图暂用项目/工厂实拍占位，替换同名图片即可；正文中的年份、厚度等参数如与最新产品不符，请直接改文字。
- 新增文章：在 `_source/posts.json` 里加一条（slug/title/date/date_iso/excerpt/image/category/blocks），再跑 `_source/build_blog.py` 重新生成；首页 3 张卡片由 `_source/add_blog_section.py` 生成（已写入，重复运行会跳过）。

### Journal 配图（产品渲染版）

6 篇文章的配图是「场景 + 产品渲染 + 编号细节」的版式（`assets/img/journal/*.jpg`，1600×900）：

- 左侧：真实项目/工厂照片 + 文章短标题；下方白底 Details 区列出 3 条细节说明（排水、型材、玻璃等）。
- 右侧：产品渲染图（白底/黑框推拉门、折叠门、白色平开窗，来自 `assets/img/renders/`），图上用 ①②③ 圆点标出对应部件。
- 右下角：该篇的关键数字（5.0 / 3.0 / 20 / 100 / 400 / RAL）。

生成方式：`_source/build_posters2.py` 定义每篇的场景图、产品图、标题、3 条细节和圆点坐标；用 Edge 无头模式按 1600×900、2 倍像素渲染，再降到 1600×900 JPEG（每张约 130–180 KB）。

替换/新增：把实拍或渲染图放进 `assets/img/renders/`，在脚本 `POSTS` 里改 `render` / `scene` / `rows` / `dots`，重跑脚本并批量截图即可。

### Contact Us

`contact-us/index.html`（页眉 Contact Us 直接进入；手机端在菜单里）：

- 页头：一句话定位 + 三条服务承诺（1 个工作日内回复 / FOB·CIF·DDP / 支持 CAD·DWG）
- 四联联系方式：邮箱、WhatsApp、电话、工厂地址（均可直接点击拨号 / 发消息 / 写邮件）
- 询盘表单（与首页同一套字段与校验），本页的 Get A Quote 会跳到本页表单
- **Social Media** 行：WhatsApp / Facebook / YouTube / Instagram / TikTok 五个品牌色圆形图标（页脚同步为同五个，悬停变品牌色）
- 社媒链接目前只有 WhatsApp 是真实可用的（`wa.me/8617818819386`）；其余四个挂 `data-coming-soon`，点击会提示"profile link to be added"。拿到账号主页地址后，替换 `_source/icons.py` 里 `SOCIALS` 的链接并重跑 `build_contact.py` 即可。

### 首页产品网格（2026-11 改版）

`#systems` 区块现在是 3×3：01–08 用实景产品照（`assets/img/products-photo/`，4:3，已裁掉图内文字与生成水印），第 09 格是深蓝色的 **Browse all products** 入口（大号 "12 / opening systems in total" + 箭头），点击本应进入 `products/index.html`——该页尚未创建，暂时挂 `data-coming-soon` 提示。

原 10–12（入户门 / 中轴门 / 折叠门）已从首页移除，等产品页建好后统一在那边展示。手机端网格为两列，Browse 卡片自动占满整行。

### 两色标题（.hl）

大标题里的关键词用 `<span class="hl">…</span>` 包裹，颜色取品牌深蓝 `--navy`，其余保持近黑，形成两色对比，避免整页黑白灰。

- 规则：整句/整段短句优先（如 "One engineering standard."），单词则只挑实词（如 "assumed"、"Foshan"）。
- 首页直接改 `index.html`；About / Blog / Contact 的标题在 `_source/build_about.py`、`build_blog.py`、`build_contact.py` 里，文章标题的强调词存在 `posts.json` 的 `accent` 字段。
- 不要在深色底（hero、页脚）上用 `.hl`，深蓝在深底上不可见。

### 产品页（products/）

三层结构，全部由脚本生成，不要手改 HTML：

| 页面 | 路径 | 数量 |
|---|---|---|
| 产品总览（12 类，按 4 组） | `products/index.html` | 1 |
| 类别页（每类 6 个型号 + 报价弹窗） | `products/<category>/index.html` | 12 |
| 产品详情页 | `products/<category>/<product>.html` | 72 |

- 数据：`_source/products_data.py`（类别文案、每组 6 个型号的名称/一句话卖点/两条差异参数/尺寸）。
- 构建：`python _source/build_products.py`，会重新生成 85 个页面；改文案或加型号只改数据文件。
- 图片：目前全部是**占位块**（`.ph`，虚线框 + 尺寸标注）。真图到位后，把 `<span class="ph">…</span>` 换成 `<img src="...">` 即可，卡片比例已按 4:3 固定；详情页主图 4:5、细节图 1:1。
- 报价弹窗：每个 `Get a quote` 按钮带 `data-name / data-code / data-specs`，`main.js` 里的 `[data-quote]` 处理函数把左侧配置和右侧表单填好；弹窗每页只有一份，避免重复 id。
- 导航：页眉 Products 下拉、手机菜单、首页 01–09 卡片都已指向对应类别页；09 卡片指向 `products/index.html`。

### Products 导航项

页眉的 **Products** 现在是真链接（`<a href="products/index.html" aria-haspopup="true">`），不是纯按钮：

- 鼠标悬停 / 键盘聚焦 → 展开 12 类下拉；
- 点击文字 → 直接进入 `products/index.html`；
- 在产品页上，它会自动带上 `is-active` 下划线（`_source/build_products.py` 里的 `chrome()` 负责，深度重写前打标）。

### 搜索浮层

搜索浮层里的 12 条产品现在是真链接，直接进入对应的类别页（`products/<category>/index.html`），不再是跳到首页的 `#catalogue`。

- 链接写在 `index.html` 的 `#search-results` 里，`build_about.py` 的 `rebase()` 会自动按页面深度补 `../`，所以二级、三级页面同样可用。
- 悬停时整行反白（深蓝底 + 白字）并在右侧出现箭头，提示可点击。
- 输入框仍按 `data-name` 过滤，Esc 关闭。

### 集合卡片点击（修复记录）

现象：手机上点卡片能跳转，电脑上点没反应。

原因：集合条原来支持「鼠标按住拖动滚动」，这段逻辑监听 `pointerdown`，只要指针移动超过 4px 就把随后的 click `preventDefault()`。鼠标点击时 1–2px 的手抖 + 图片原生拖拽都会被算成拖动，于是跳转被吃掉。触屏走的是另一条分支（`pointerType === "touch"` 直接 return），所以手机正常。

处理：

1. **删掉鼠标拖动滚动**（`.rail` 的 pointerdown/move/up 代码块）。集合条改用两侧箭头按钮、滚轮、触控板横向滑动滚动 —— 这些都不影响点击。
2. 卡片图片加 `draggable="false"` 与 `-webkit-user-drag: none`，杜绝原生图片拖拽。
3. 「By opening」四张卡改为 `<article>` + 内层 `<a class="rail-card__link">` + 独立 `<a class="rail-card__cta--link">`，CTA 是真链接；「By application」结构相同，CTA 指向联系页。

改动在 `assets/js/main.js`，客户端可能缓存旧脚本 —— 改完要 **Ctrl+F5 硬刷新** 才能生效。

### 目录卡片（Catalogue）

`#catalogue` 的 8 张产品卡：

- **整张卡不再可点**：图片和产品名都是普通元素，只有悬停面板里的两个按钮是链接 —— `View details`（进产品详情）、`Request A Quote`（去询盘）。
- 两个按钮并排、间距 6px，卡片窄时自动换行；手机（≤760px）改为单列，按钮等宽。
- **触屏没有 hover**：`@media (hover: none), (max-width: 760px)` 下悬停面板变成静态块，规格和按钮常显，不再"藏在悬停里"。
- 手机端右下角悬浮的 `GET A QUOTE` 缩小到 40px 高并加了 `main` 的底部留白，仍可能遮住刚好滚到该位置的按钮 —— 这是固定悬浮按钮的固有取舍，需要的话可以做成滚动时自动隐藏。

### 样式缓存

`style.css` 的链接带了 `?v=<mtime>`（97 个页面全部处理）。改完样式后运行一次 `_source/cachebust.py` 里的逻辑（或重新执行同一段脚本）刷新版本号，浏览器就会取新文件，不用再按 Ctrl+F5。

### 重复区块（修复记录）

`#collections` 曾经出现两次：一份只有标题 + 标签栏的空壳，一份完整。原因是早前用索引切片改这段 HTML 时，切片边界落在 `</section>` 之后，把标题栏又插了一遍。空的重复块还带重复 id（`tab-opening`、`panel-opening`），会让标签切换绑定到没有面板的那一份上。

已删除空壳，现在全站 HTML **重复 id 为 0**。以后改完首页可以做一次体检：

```python
# 统计每个 html 里重复出现的 id
```

### 页脚与悬浮按钮

页脚底栏（版权 / Privacy / Terms / 社媒图标）会被右下角固定的 `GET A QUOTE` 挡住，处理：

- 桌面：`.footer__bottom { padding-right: 210px }`，把这一行整体左移，给悬浮按钮让出位置。
- 手机（≤980px）：改为 `padding-bottom: 74px`，图标行整体抬高，悬浮按钮落在它下方。

实测（滚到页面最底）：
- 1440 宽：按钮 x 1255–1412，图标 x 985–1167 → 间�88px，不重叠
- 390 宽：按钮 y 792–832，图标 y 668–698 → 上下错开，不重叠

### 社媒链接清单

| 平台 | 地址 | 状态 |
|---|---|---|
| WhatsApp | `https://wa.me/8617818819386` | 已生效（等同 `api.whatsapp.com/send?phone=8617818819386`） |
| Facebook | `https://www.facebook.com/profile.php?id=61594390266054` | 已生效 |
| YouTube | — | 占位，点击提示"待补充" |
| Instagram | — | 占位 |
| TikTok | — | 占位 |

改链接只改 `_source/icons.py` 的 `SOCIALS`（Contact 页社媒行）和 `index.html` 页脚的 `footer__social`（各页页脚由此继承），然后重跑 build_about / build_blog / build_contact / build_products。

### 案例页（cases/）

两级结构，脚本生成：

| 页面 | 路径 | 数量 |
|---|---|---|
| 案例列表 | `cases/index.html` | 1 |
| 项目详情 | `cases/<slug>.html` | 6 |

- 数据：`_source/cases_data.py`（地点、类型、系统、事实条、三段正文、标题强调短语 `hl`）。
- 构建：`python _source/build_cases.py`。页面在 `cases/` 下一级，所以**相对路径按一级目录**生成（`../assets/`），`file://` 打开也能正常加载样式。
- 首页 `#cases` 的六张图分别链到对应项目页；「All case studies」和页眉 `Cases` 指向列表页。
- 详情页右侧「System used」链到对应产品类别页，形成 案例 → 产品 的互链；底部是上一个/下一个 + 另外三个项目。

### 真实产品数据（Aluminium Sliding Doors）

这个类别不再用手写占位产品，改为抓取原站 `/supplier-4782834-aluminium-sliding-doors` 的 16 个真实在售产品：

- `_source/scrape_sliding.py`：抓标题、6 项商务参数（Brand / Model / MOQ / Price / Delivery / Payment）、简介正文、产品图，写入 `_source/source_products.json`，图片存 `assets/img/products-src/`。
- `_source/apply_source_products.py`：把这些记录转成产品页数据结构（卡片、详情、报价弹窗都用它）。
- 类别页现在显示 16 张真实卡片（图 + 标题 + MOQ + 价格）；详情页是「图 + Specification & terms 表 + Product description + 配置项」。
- 价格/交期是原站公开数据（USD85–135/m²、MOQ 4–6 m²、25–35 天），要改价直接改 `source_products.json` 或页面数据后重跑构建。
- 其余 11 个类别仍是占位数据，需要的话按同样方式抓取（改 `scrape_sliding.py` 里的 LIST 常量）。

### 类别页分页

产品超过 6 个的类别自动分页（目前只有 Aluminium Sliding Doors，16 个）：

- 构建时给网格加 `data-per-page="6"`，并在网格后放一个空的 `<nav class="ppager" data-pager>`；
- `main.js` 里的分页脚本按 6 个一页切分、生成「← Prev / 1 2 3 / Next →」，点击切换并平滑滚回网格顶部；
- 只有一页时（≤6 个产品）分页条自动隐藏，其他 11 个类别不受影响；
- 所有卡片仍在同一页面的 HTML 里（只做显隐），不新增 URL，SEO 和 file:// 预览都正常。

产品详情页底部「Other …」关联卡片也改成取真实产品图（有图就用图，无图才用占位块）。

### 多类别抓取（通用）

`_source/scrape_category.py` 已通用化，任何类别都能抓：

```
python _source/scrape_category.py <source_id> <category-slug> <输出文件名>
# 例：滑动窗
python _source/scrape_category.py 4782833 aluminium-sliding-windows source_windows.json
```

抓完把「类别 slug → json 文件名」登记到 `_source/apply_source_products.py` 的 `SOURCES`，重跑 `build_products.py`，再用 `finalize_category.py` 清理旧页面并刷新 sitemap。

当前已接入：

| 类别 | 产品数 | 分页 |
|---|---|---|
| Aluminium Sliding Doors | 41 | 7 页 |
| Aluminium Sliding Windows | 90 | 15 页 |

类别页的标题数量、价格区间、chips、导语全部由数据推导；产品卡数量超过 6 个自动分页。

### 手动补图（源站缺图的产品）

抓取时个别产品源站没有图（滑动窗里有 2 个）。补法：

1. 把图片存为 `assets/img/products-src/<slug>.jpg`；
2. 在 `_source/source_windows.json` 里给对应记录填 `local_image`；
3. 重跑 `build_products.py` + `finalize_category.py <slug>`。

这两个产品：`good-quality-cheap-prices-aluminum-broken-bridge-sliding-windows-and-d`（MODEL 90 SW）、
`anti-mosquito-screen-commercial-aluminum-sliding-windows-with-multiple`（MODEL WEIJIA SW）。

### 类别封面图

`products/index.html` 上 12 张类别卡片的封面：

- 8 个类别直接用首页那 8 张实拍图（`assets/img/products-photo/*.jpg`），映射表在 `_source/build_products.py` 的 `CAT_PHOTO`；
- 没有专属图的 4 个类别（平开门、卫浴门、入户门、中轴门）自动取该类第一个产品的实拍图；
- 全都没有图时才会退回虚线占位块。改图只需换 `CAT_PHOTO` 里的路径后重跑 `rebuild_all.py`。

### 产品详情页（定型版）

版式已定，勿随意改动：

1. **主图区**：左侧固定 4:3 画框（`object-fit: contain`，切换图片不位移），右侧竖排 96px 缩略图条，点击切换，当前项深蓝描边；只有一张图时整条隐藏。
2. **Specification & terms**：6 项商务条款（Brand / Model / MOQ / Price / Delivery / Payment）。
3. **Spec 参数区**：`Detail Information` 与 `Specifications` 两张表**上下排列**，表内每行两组“标签 + 值”，细线分隔、小号大写标签。
4. **Description**：左侧概括正文 + 要点列表（粗体标题 + 破折号），右侧源站结构图，多图时 `← 1 / 3 →` 切换。

数据来源与文件：

- `_source/scrape_details.py` → `_source/source_details.json`（每产品：detail / spec_rows / desc_paras / features / gallery[相册] / desc_files[结构图]）
- 相册图存 `assets/img/products-detail/<slug>-g*.jpg`，结构图存 `<slug>-d*.jpg`（宽度上限 1000px）
- `_source/backfill_gallery.py` 给老记录补相册
- `_source/product_detail_blocks.py` 负责渲染，`build_products.py` 调用
