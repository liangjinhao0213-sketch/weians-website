# 全站检测报告

日期：2026-11-06　范围：静态站 447 页 + WordPress 467 个 URL

## 一、检测方法

| 项目 | 静态站 | WordPress |
|---|---|---|
| 页面抓取 | 直接解析 447 个 HTML | 按 sitemap + 额外页面，逐页 GET |
| 内链 | 解析所有 href，按相对路径解析后验存在 | 同上（HTTP 200 判定） |
| 锚点 | `#id` 是否在该页存在 | — |
| 资源 | img / srcset / css / js 是否存在 | 1413 张 wp-content 图片逐张 HEAD |
| 元数据 | title / description 是否重复或缺失 | 同左 |
| 代码错误 | — | 扫描 Fatal / Warning / Notice / Deprecated |

## 二、修复前发现的问题

| # | 问题 | 影响范围 | 严重度 |
|---|---|---|---|
| 1 | 页脚 `/privacy/`、`/terms/` 指向不存在的页面 | 静态 446 页 + WP 全站 | 高 |
| 2 | 28 处 meta description 里有**未转义的英文引号**，属性被截断（读出来只有 "A "） | 14 个产品页 | 高 |
| 3 | `/downloads/ws90-datasheet.pdf` 文件不存在 | 首页 | 中 |
| 4 | Videos 页面导航指向 `videos/index.html`（自指错误） | 3 处（videos 页内） | 中 |
| 5 | 一个产品被收录两次（标题、内容完全相同） | 静态 1 页 + WP 1 个产品 | 中 |
| 6 | 1 个 title 含裸 `&` 未转义 | 1 个产品页 | 低 |
| 7 | 静态 sitemap 缺 privacy / terms / videos，且含已删除的重复产品 | sitemap.xml | 中 |
| 8 | privacy / terms 页导航高亮错标为 Cases；videos 页没有高亮 | 3 页 | 低 |

## 三、已修复

1. **新建 Privacy Policy 与 Terms of Use 两个页面**（静态 + WordPress 各一套，`page-privacy.php` / `page-terms.php`），页脚链接改为真实地址，去掉"敬请期待"提示
2. **28 处 meta 引号转义为 `&quot;`**，14 个产品页的描述恢复完整
3. **生成 WS-90 技术数据表 PDF**（18 项参数，254 KB），首页链接改为直接下载
4. **修正 videos 页自指链接**
5. **删除重复产品** `perfect-system-...-f-2`（静态页 + WP 文章 #792），分类页链接改指正规页；重新导出 `products-import.json`（413 → 412）
6. **修正 1 个 title 的裸 `&`**
7. **重建静态 sitemap**：447 条，与实际文件一一对应（0 缺失）
8. **修正导航高亮**：privacy/terms 不再误高亮 Cases，videos 页正确高亮

## 四、修复后复检

```
静态站（447 页）
  死链            0
  断锚点          0
  重复 title      0
  重复 description 0
  图片缺 alt      0
  重复 id         0
  空 href="#"     0

WordPress（467 个 URL）
  非 200          0
  PHP 报错        0
  缺 title        0
  缺 description  0
  图片缺失        0 / 1413
```

## 五、仍建议处理（不影响当前使用）

| 事项 | 说明 |
|---|---|
| 两组"同名不同内容"产品 | `thermal-insulated-...performa` 与 `-2`、`heavy-duty-sound-insulated-...entrance-d` 与 `-2`：名称只有大小写差异，但参数行数不同（26 vs 29）。属于源站重复上架，建议人工比对后保留一个 |
| 静态站图片体积 107 MB | 产品原图未压缩，上线后建议批量压到 1200px |
| 静态站无 404 页面 | 部署后建议配一个品牌化 404 |
| 多语言 | 之前已按要求停用 |

## 六、复检命令

```bash
python _source/audit_static.py    # 静态站
python _source/audit_wp.py        # WordPress
```
