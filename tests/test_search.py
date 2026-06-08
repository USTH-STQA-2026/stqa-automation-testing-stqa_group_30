"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
      (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
      (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
      (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
        (*Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.*)

    Hints (*Gợi ý*):
        - login(page, test_config)
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
        - Verify: page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)
    pytest.skip("Not implemented — student must complete (Chưa hoàn thành)")


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
        (*Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.*)

    Hints (*Gợi ý*):
        - Verify: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count() == 0
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)
    pytest.skip("Not implemented — student must complete (Chưa hoàn thành)")


def test_filter_by_category_uppercase(page, test_config):
    """TC-06b: Filter books by category — UPPERCASE input
    (*Lọc sách theo thể loại — nhập VIẾT HOA "CÔNG NGHỆ"*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    📖 RIPR Model: xem comment [R], [I], [P], [R✓] bên dưới.

    🎯 Mục tiêu (Equivalence / Robustness testing):
        Kiểm tra bộ lọc có PHÂN BIỆT HOA-THƯỜNG hay không.
        Nhập "CÔNG NGHỆ" (viết hoa) phải cho ra CÙNG kết quả với "Công nghệ".
        → Đây là test đối chứng (oracle) cho tính năng lọc không phân biệt hoa-thường.

    ⚠️ Giả định: hệ thống lọc KHÔNG phân biệt hoa-thường (case-insensitive),
        đây là hành vi thông dụng và thân thiện người dùng.
        Nếu SRS yêu cầu lọc PHÂN BIỆT hoa-thường, đảo lại assert cuối (mong đợi 0 sách).
    """
    SEARCH_TERM = "CÔNG NGHỆ"          
    EXPECTED_CATEGORY = "Công nghệ"     

    login(page, test_config)

    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        SEARCH_TERM,
    )

    try:
        page.locator(
            'flt-semantics[role="group"][aria-label*="Công nghệ"], '
            'flt-semantics[aria-label*="Công nghệ"]'
        ).last.wait_for(state="attached", timeout=15000)
    except Exception:
        pass
    enable_flutter_semantics(page)
    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "filter_category_uppercase.png")
    )

    book_cards = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"], '
        'flt-semantics[aria-label*="Mã: BOOK"]'
    )
    labels = [
        book_cards.nth(i).get_attribute("aria-label") or ""
        for i in range(book_cards.count())
    ]

    assert len(labels) > 0, (
        f"Uppercase filter '{SEARCH_TERM}' returned 0 books — filter may be "
        f"case-SENSITIVE (Lọc viết hoa '{SEARCH_TERM}' không ra sách nào — "
        f"bộ lọc có thể đang PHÂN BIỆT hoa-thường, không thân thiện người dùng)"
    )

    wrong_books = [lbl for lbl in labels if EXPECTED_CATEGORY not in lbl]
    assert not wrong_books, (
        f"Filter leaked {len(wrong_books)} non-'{EXPECTED_CATEGORY}' book(s): "
        f"{wrong_books} (Bộ lọc để lọt {len(wrong_books)} sách sai thể loại)"
    )

    print(
        f"\n[TC-06b] OK — uppercase '{SEARCH_TERM}' → {len(labels)} book(s), "
        f"all in '{EXPECTED_CATEGORY}' (lọc không phân biệt hoa-thường ✔)"
    )


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    📖 RIPR Model: xem comment [R], [I], [P], [R✓] bên dưới.

    📋 SRS REQ-03 (Tìm kiếm theo tên sách hoặc tác giả):
        Seed data — tác giả "Nguyễn Minh Đức" có 2 sách:
            • BOOK001 — Lập trình Flutter cơ bản
            • BOOK009 — Nhập môn lập trình Python
        Test Oracle: tìm tác giả này phải ra ÍT NHẤT 1 kết quả, và MỌI sách
        hiển thị đều có tên tác giả trong aria-label (search không để lọt sách lạ).
    """
    AUTHOR = "Nguyễn Minh Đức"

    login(page, test_config)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        AUTHOR,
    )

    try:
        page.locator(
            f'flt-semantics[aria-label*="{AUTHOR}"]'
        ).last.wait_for(state="attached", timeout=15000)
    except Exception:
        pass
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author.png"))

    author_hits = page.locator(f'flt-semantics[aria-label*="{AUTHOR}"]').count()
    assert author_hits > 0, (
        f"No results for author '{AUTHOR}' "
        f"(Không tìm thấy kết quả cho tác giả '{AUTHOR}')"
    )

    book_cards = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"], '
        'flt-semantics[aria-label*="Mã: BOOK"]'
    )
    labels = [
        book_cards.nth(i).get_attribute("aria-label") or ""
        for i in range(book_cards.count())
    ]
    assert len(labels) > 0, (
        f"Author found in text but no book card displayed "
        f"(Thấy tên tác giả nhưng không có card sách nào hiển thị)"
    )
    wrong_books = [lbl for lbl in labels if AUTHOR not in lbl]
    assert not wrong_books, (
        f"Search leaked {len(wrong_books)} book(s) by other authors: {wrong_books} "
        f"(Tìm kiếm để lọt {len(wrong_books)} sách của tác giả khác)"
    )

    print(f"\n[TC-07] OK — author '{AUTHOR}' → {len(labels)} book(s) found")
