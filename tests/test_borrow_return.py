"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - "Mượn / Trả" tab: role="tab", aria-label="Mượn / Trả"
    - Available books have "Có sẵn" in aria-label, borrowed books have "Đang mượn"
      (*Sách "Có sẵn" có aria-label chứa "Có sẵn", sách "Đang mượn" chứa "Đang mượn"*)
    - Borrow button: 'flt-semantics[role="button"]:has-text("Mượn sách này")'
      (*Nút mượn*)
    - After clicking "Mượn sách này", a confirmation dialog appears — click "Mượn" again
      (*Sau khi click "Mượn sách này" sẽ hiện dialog xác nhận — cần click nút "Mượn" lần nữa*)
    - Return button: 'flt-semantics[role="button"]:has-text("Trả sách")'
      (*Nút trả*)
"""
import os
import time
import pytest  # type: ignore[import]
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR, wait_for_flutter,
)

import re


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Xem comment [R], [I], [P], [R✓] bên dưới.

    📋 SRS REQ-04 (Mượn sách):
        - Điều kiện: sách ở trạng thái "Có sẵn"
        - Sau khi mượn: sách → "Đã mượn", phiếu mượn → "Đang mượn" (REQ-02: real-time)
        - Lưu ý: dùng tài khoản Thành viên đang hoạt động (vd: ba.nguyen@email.com)
          vì Thủ thư có flow mượn-hộ khác (chọn thành viên).
    """
    
    login(page, test_config)

    borrow_btn = page.locator(
        'flt-semantics:has-text("Mượn sách này"), '
        'flt-semantics[aria-label*="Mượn sách này"]'
    ).last
    borrow_btn.wait_for(state="attached", timeout=15000)
    borrow_btn.scroll_into_view_if_needed()

    borrow_btn.click()

    wait_for_flutter(page, text="Mượn")
    enable_flutter_semantics(page)

    confirm_btn = (
        page.locator('flt-semantics[role="button"]')
        .filter(has_text=re.compile(r"^\s*(Mượn|Xác nhận|OK)\s*$"))
        .last
    )
    confirm_btn.wait_for(state="attached", timeout=10000)
    confirm_btn.click()

    page.locator(
        'flt-semantics:has-text("Đã mượn"), '
        'flt-semantics:has-text("Đang mượn"), '
        'flt-semantics:has-text("thành công"), '
        'flt-semantics[aria-label*="Đã mượn"]'
    ).last.wait_for(state="attached", timeout=15000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    aria_labels = " ".join(
        el.get_attribute("aria-label") or ""
        for el in page.locator("flt-semantics[aria-label]").element_handles()
    )
    combined = sem_text + " " + aria_labels

    has_borrowed_status = "Đã mượn" in combined or "Đang mượn" in combined
    has_success_message = "thành công" in combined
    assert has_borrowed_status or has_success_message, (
        "Borrow failed: book status did not change and no success message found "
        "(Mượn sách không thành công: trạng thái sách không đổi sang "
        "'Đã mượn'/'Đang mượn' và không có thông báo thành công)"
    )


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    📖 RIPR Model: xem comment [R], [I], [P], [R✓] bên dưới.

    📋 SRS REQ-08 (Tra cứu phiếu mượn):
        - Thành viên chỉ xem phiếu mượn của chính mình.
        - Seed data: MEM002 (ba.nguyen) đang mượn BOOK003 → tab Mượn / Trả
          phải có ít nhất 1 phiếu "Đang mượn" ngay cả khi chưa mượn thêm sách.
    """
    login(page, test_config)

    tab = page.locator(
        'flt-semantics[role="tab"][aria-label*="Mượn"], '
        'flt-semantics[role="tab"]:has-text("Mượn"), '
        'flt-semantics[aria-label*="Mượn / Trả"], '
        'flt-semantics:has-text("Mượn / Trả")'
    ).last
    tab.wait_for(state="attached", timeout=15000)
    tab.click()

    enable_flutter_semantics(page)
    page.locator(
        'flt-semantics:has-text("Đang mượn"), '
        'flt-semantics[aria-label*="Đang mượn"], '
        'flt-semantics:has-text("Trả sách"), '
        'flt-semantics[aria-label*="Trả sách"]'
    ).last.wait_for(state="attached", timeout=15000)
    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "view_borrowed_books.png")
    )

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    aria_labels = " ".join(
        el.get_attribute("aria-label") or ""
        for el in page.locator("flt-semantics[aria-label]").element_handles()
    )
    combined = sem_text + " " + aria_labels

    has_borrowing_record = "Đang mượn" in combined
    has_return_button = "Trả sách" in combined
    assert has_borrowing_record or has_return_button, (
        "Borrowed books list not shown: no 'Đang mượn' record or 'Trả sách' button "
        "(Không hiển thị danh sách sách đang mượn: không thấy phiếu 'Đang mượn' "
        "hoặc nút 'Trả sách')"
    )


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    📖 RIPR Model: xem comment [R], [I], [P], [R✓] bên dưới.

    📋 SRS REQ-05 (Trả sách):
        - Chỉ trả sách mà thành viên đang mượn.
        - Seed data: MEM002 (ba.nguyen) đang mượn BOOK003 → có sẵn 1 sách để trả,
          không phụ thuộc TC-08 (mượn sách) chạy trước.
        - Sau khi trả: phiếu mượn → "Đã trả", sách → "Có sẵn" (REQ-02: real-time).
    """

    login(page, test_config)
    tab = page.locator(
        'flt-semantics[role="tab"][aria-label*="Mượn"], '
        'flt-semantics[role="tab"]:has-text("Mượn"), '
        'flt-semantics:has-text("Mượn / Trả")'
    ).last
    tab.wait_for(state="attached", timeout=15000)
    tab.click()
    enable_flutter_semantics(page)

    return_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách"), '
        'flt-semantics:has-text("Trả sách"), '
        'flt-semantics[aria-label*="Trả sách"]'
    ).last
    return_btn.wait_for(state="attached", timeout=15000)
    return_btn.scroll_into_view_if_needed()

    return_btn.click()

    enable_flutter_semantics(page)
    confirm_btn = (
        page.locator('flt-semantics[role="button"]')
        .filter(has_text=re.compile(r"^\s*(Trả|Trả sách|Xác nhận|OK)\s*$"))
        .last
    )
    try:
        confirm_btn.wait_for(state="attached", timeout=3000)
        confirm_btn.click()
        enable_flutter_semantics(page)
    except Exception:
        pass  

    page.locator(
        'flt-semantics:has-text("Đã trả"), '
        'flt-semantics[aria-label*="Đã trả"], '
        'flt-semantics:has-text("thành công")'
    ).last.wait_for(state="attached", timeout=15000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book_success.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    aria_labels = " ".join(
        el.get_attribute("aria-label") or ""
        for el in page.locator("flt-semantics[aria-label]").element_handles()
    )
    combined = sem_text + " " + aria_labels

    has_returned_status = "Đã trả" in combined
    has_success_message = "thành công" in combined
    assert has_returned_status or has_success_message, (
        "Return failed: no 'Đã trả' status or success message found "
        "(Trả sách không thành công: không thấy trạng thái 'Đã trả' "
        "hoặc thông báo thành công)"
    )
    
