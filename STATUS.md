# 进度快照

更新：2026-11-03 — 产品详情页改版完成、图片压缩与去重完成

## 站点规模

| 项目 | 数值 |
|---|---|
| 页面 | 445（首页 + 12 类别 + 413 产品 + About/Blog/Cases/Contact） |
| 产品 | 413，全部真实数据 |
| 图片 | 3500+ 张 |
| 总大小 | **163.8 MB**（原 224 MB） |
| 断链 | 0 |

### 体积构成

| 目录 | 大小 | 说明 |
|---|---|---|
| assets/img/products-src | 62.7 MB | 413 张产品主图（首页目录卡也在用，**未压缩**） |
| assets/img/products-detail | 36.9 MB | 1080 张详情图（已压缩 + 去重，原 102 MB） |
| assets/img（根目录） | 4.3 MB | 首页大图、案例、logo |
| assets/img/products-photo | 1.8 MB | 12 张类别封面（未压缩） |
| 其余 | ~2 MB | 字体、CSS、JS、日志图 |

## 产品详情页（定型版式）

1. 主图区：固定 4:3 画框 + 右侧竖排 96px 缩略图（切换不位移）
2. Specification & terms：6 项商务条款
3. Spec 参数区：Detail Information + Specifications 上下两张表
4. Description：左文右图 + 多图箭头切换

## 图片处理记录

- 详情图统一压到宽 800px / 质量 72
- 3222 张里只有 1080 张唯一：其余 2142 张是同一批结构图被多个产品重复引用
- 已改为「按内容哈希命名（`u<md5前12位>.jpg`）」，413 个产品共用同一份文件
- 因此 **zip 打包后也是 36.9 MB**，不再是表面 96 MB

## 维护命令

```bash
python _source/scrape_rest.py         # 抓取/续抓类别产品
python _source/scrape_details.py      # 抓详情参数 + 相册 + 结构图（可续传）
python _source/backfill_gallery.py    # 给老记录补相册
python _source/refill_images.py       # 补下载失败的图片
python _source/rebuild_all.py         # 重建全部页面 + 清旧文件 + sitemap + 缓存
```

## 可选后续

- `products-src`（62.7 MB）仍是大头，但首页目录卡在用，压缩会影响首页 → 暂不动
- 若要进一步瘦身：只压缩「非首页那 8 张」的产品主图，预计可降到 ~120 MB
