---
{
  "id": "crawler-文字层检测和OCR路-006",
  "domain": "crawler",
  "source": "knowledge/crawler/04-pdf-parameter-locator.md",
  "q": "文字层检测和 OCR 路线分别用什么工具？",
  "a": "文字层用 PyMuPDF（最快，0.12s/59 页）或 pymupdf4llm；OCR 用 Tesseract 5.5 + chi_sim。EasyOCR 作为 OCR 替代方案（pip 全自动但含 PyTorch ~500MB）。",
  "created": "2026-07-21",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-21",
  "reviews": 0
}
---

**Q**: 文字层检测和 OCR 路线分别用什么工具？

**A**: 文字层用 PyMuPDF（最快，0.12s/59 页）或 pymupdf4llm；OCR 用 Tesseract 5.5 + chi_sim。EasyOCR 作为 OCR 替代方案（pip 全自动但含 PyTorch ~500MB）。
