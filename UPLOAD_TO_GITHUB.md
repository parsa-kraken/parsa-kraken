# راه‌اندازی Profile README

این پروژه برای Profile README گیت‌هاب آماده است.

## 1) نام Repository

در GitHub یک Repository **Public** بساز که نامش دقیقاً برابر username اکانتت باشد.

برای اکانت فعلی این پروژه:

`parsa-kraken`

بنابراین نام repository نیز باید:

`parsa-kraken`

باشد.

## 2) فایل‌ها

تمام فایل‌ها و پوشه‌های داخل این ZIP را در ریشه همان Repository قرار بده؛ مخصوصاً:

- `README.md`
- `dark.svg`
- `light.svg`
- `dist/github-jet.svg`
- `generate.mjs`
- `.github/workflows/jet-heatmap.yml`

پوشه `.github` مخفی نیست؛ باید دقیقاً با همین نام و ساختار آپلود شود.

## 3) اولین اجرای Live Contributions

بعد از Commit/Upload:

1. وارد تب **Actions** Repository شو.
2. Workflow با نام **Sync live contribution heatmap** را باز کن.
3. **Run workflow** را بزن.
4. پس از پایان موفق Workflow، فایل `dist/github-jet.svg` با contributionهای واقعی همین اکانت ساخته می‌شود.

پس از آن Workflow روزانه اجرا می‌شود و نمودار را به‌روز می‌کند.

## 4) تطبیق خودکار با اکانت

Workflow از مقدار زیر استفاده می‌کند:

`github.repository_owner`

بنابراین contribution graph به‌صورت خودکار از صاحب همان Repository خوانده می‌شود و username داخل workflow hard-code نشده است.

## 5) Private contributions (اختیاری)

حالت پیش‌فرض از `GITHUB_TOKEN` خود GitHub Actions استفاده می‌کند و برای داده‌های قابل دسترس آن token کافی است.

اگر بعداً لازم شد داده‌ای را بخوانی که token پیش‌فرض به آن دسترسی ندارد، می‌توانی در Repository Settings > Secrets and variables > Actions یک secret با نام زیر اضافه کنی:

`PROFILE_TOKEN`

Workflow در صورت وجود، `PROFILE_TOKEN` را مقدم بر `GITHUB_TOKEN` استفاده می‌کند.

فقط حداقل سطح دسترسی موردنیاز را به token بده و هیچ tokenای را داخل فایل‌های repository قرار نده.

## 6) نکته درباره «Live»

GitHub README کد JavaScript دلخواه را در صفحه Profile اجرا نمی‌کند. چیزی که این پروژه انجام می‌دهد این است:

- UI اصلی از SVGهای `dark.svg` و `light.svg` رندر می‌شود.
- انیمیشن‌های مجاز خود SVG نمایش داده می‌شوند.
- GitHub Actions داده contribution واقعی اکانت را می‌گیرد.
- SVG contribution دوباره ساخته و داخل repository commit می‌شود.
- README همیشه آخرین SVG موجود در repository را نشان می‌دهد.

پس بخش contribution واقعاً با داده GitHub همگام است، اما این همگام‌سازی دوره‌ای است، نه اجرای JavaScript لحظه‌ای در مرورگر.
