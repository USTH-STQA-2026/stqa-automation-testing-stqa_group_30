"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.

(*File này chứa 1 ví dụ mẫu (TC-01) đã hoàn chỉnh.
Sinh viên cần hoàn thành TC-02 và TC-03.*)
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    (*ĐÃ HOÀN THÀNH — Dùng làm ví dụ tham khảo.*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Mỗi dòng code trong test tương ứng với 1 bước trong chuỗi RIPR.
        Xem comment [R], [I], [P], [R✓] bên dưới.
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail – wrong password (*Đăng nhập thất bại – sai mật khẩu*)

    🔴 NOT COMPLETED — Students must implement this test case.
    (*CHƯA HOÀN THÀNH — Sinh viên cần viết code cho test case này.*)

    Description (*Mô tả*):
        Enter correct email but wrong password → system stays on login page
        or shows an error message.
        (*Nhập email đúng nhưng mật khẩu sai → hệ thống không chuyển trang,
        hoặc hiển thị thông báo lỗi.*)

    📖 RIPR — Áp dụng cho test case này:
        [R] page.goto(...) → Chạm tới trang đăng nhập
        [I] flutter_fill(..., "wrongpassword") → Nhiễm trạng thái lỗi
        [P] Hệ thống xử lý login → Lỗi lan truyền ra thông báo
        [R✓] assert ... → Test Oracle kiểm tra thông báo lỗi

    💡 Bonus B2 — Data-Driven Testing:
        TC-02 và TC-03 có cùng pattern (nhập → click → kiểm tra lỗi).
        Bạn có thể gộp bằng @pytest.mark.parametrize:

        @pytest.mark.parametrize("email, password, tc_id", [
            ("valid@email.com", "wrongpass", "TC-02"),
            ("", "", "TC-03"),
        ])
        def test_login_fail(page, test_config, email, password, tc_id):
            ...

        Xem thêm: docs/textbook-concepts.md §3 (Data-Driven Testing)

    Suggested steps (*Gợi ý các bước*):
        1. Navigate to login page (*Truy cập trang đăng nhập*)
        2. Enable Flutter semantics (*Bật Flutter semantics*)
        3. Enter correct Email (from test_config["email"]) (*Nhập Email đúng*)
        4. Enter wrong Password (e.g. "wrongpassword") (*Nhập Mật khẩu sai*)
        5. Click "Đăng nhập" (*Click "Đăng nhập"*)
        6. Assert: URL still on login page OR error message shown
           (*Assert: URL vẫn ở trang đăng nhập HOẶC có thông báo lỗi*)
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)
    
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")
    
    wait_for_flutter(page, text="Đăng nhập")
    
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_wrong_password.png"))
    
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert not has_user_name and not has_logout, \
        f"Security risk: User '{test_config['display_name']}' was logged in even with a wrong password! " \
        f"(Rủi ro bảo mật: Tài khoản vẫn đăng nhập thành công dù nhập sai mật khẩu)"


@pytest.mark.parametrize("email, password, should_pass, tc_id", [
            ("ba.nguyen@email.com", "wrongpass", False, "TC-01"),
            ("Ba.nguyen@email.com", "password123", True, "TC-05"),
            ("", "", False, "TC-03"),
])
def test_login_fail(page, test_config, email, password, should_pass, tc_id):
    target_email = test_config["email"] if email == "valid_email_placeholder" else email
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    
    flutter_fill(page, "Email", target_email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")
    
    if should_pass:
        wait_for_flutter(page, text="Đăng xuất")  
    else:
        wait_for_flutter(page, text="Đăng nhập")  
    
    status_str = "success" if should_pass else "fail"
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"login_{status_str}_{tc_id}.png"))
    
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    
    if should_pass:
        assert has_user_name or has_logout, \
            f"[{tc_id}] Error: Login should succeed but failed! " \
            f"(Đăng nhập nên thành công nhưng lại thất bại)"
    else:
        assert not has_user_name and not has_logout, \
            f"[{tc_id}] Critical: Login should fail but succeeded! " \
            f"(Đăng nhập nên thất bại nhưng lại thành công — Rủi ro bảo mật)"