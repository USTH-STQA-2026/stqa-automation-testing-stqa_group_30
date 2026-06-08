"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - Logout button: 'flt-semantics[role="button"]:has-text("Đăng xuất")'
      (*Nút Đăng xuất*)
    - Language switch EN button: 'flt-semantics[role="button"]:has-text("EN")'
      (*Nút chuyển ngôn ngữ EN*)
    - After logout: page returns to login (has "Đăng nhập" button and "Email" input)
      (*Sau đăng xuất: trang quay về login*)
    - After switching to EN: text "Logout", "Borrow", "Search", "Library" may appear
      (*Sau chuyển EN: text tiếng Anh có thể xuất hiện*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR, smart_click, wait_for_flutter,
)


def test_logout(page, test_config, web_tech):
    """TC-11: Logout success (Đăng xuất thành công)

    Description (Mô tả):
        Log in → click Logout → verify page returns to login screen.
        (Đăng nhập → click Đăng xuất → kiểm tra quay về trang đăng nhập.)
    """
    login(page, test_config)

    
    smart_click(page, "Đăng xuất", tech=web_tech)

    
    wait_for_flutter(page, text="Đăng nhập", timeout=10000)

    
    if web_tech.is_flutter_canvaskit:
        enable_flutter_semantics(page)

    
    if web_tech.is_flutter_canvaskit:
        login_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng nhập")').first
        email_input = page.locator('input[aria-label="Email"]').first
    else:
        login_btn = page.get_by_role("button", name="Đăng nhập").first
        email_input = page.get_by_label("Email").first

    
    assert login_btn.is_visible() or email_input.is_visible(), (
        "Lỗi: Không tìm thấy nút 'Đăng nhập' hoặc ô 'Email'. Có thể đăng xuất thất bại."
    )

    
    screenshot_path = os.path.join(test_config["screenshot_dir"], "logout_success.png")
    page.screenshot(path=screenshot_path)


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → click "EN" button → verify UI switches to English.
        (*Đăng nhập → click nút "EN" → kiểm tra giao diện chuyển sang tiếng Anh.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "EN" button and click (*Tìm nút "EN" và click*)
        3. Wait 2s, re-enable semantics (*Đợi 2s, bật lại semantics*)
        4. Get sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
        5. Assert: "Logout" or "Borrow" or "Library" in sem_text
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)
    pytest.skip("Not implemented — student must complete (Chưa hoàn thành)")
