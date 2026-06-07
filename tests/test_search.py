import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    wait_for_flutter,
    login,
)

SEARCH_PLACEHOLDER = "Tìm kiếm theo tên sách hoặc tác giả..."


def get_sem_text(page):
    """Lấy toàn bộ text + aria-label từ Semantics Tree."""
    elements = page.locator("flt-semantics").all()
    texts = []
    for el in elements:
        texts.append(el.inner_text() or "")
        texts.append(el.get_attribute("aria-label") or "")
    return " ".join(texts)


def test_search_book_by_exact_name(page, test_config):
    """
    TC-04a: Tìm sách bằng tên chính xác
    Input    : "Lập trình Flutter cơ bản"
    Expected : Hiển thị sách BOOK001
    """
    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(page, SEARCH_PLACEHOLDER, "Lập trình Flutter cơ bản")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    sem_text = get_sem_text(page)
    assert (
        "Lập trình Flutter cơ bản" in sem_text
    ), f"Không tìm thấy sách trong kết quả.\nSem text (500 ký tự đầu): {sem_text[:500]}"

    page.screenshot(path=f"{test_config['screenshot_dir']}/tc04a_search_exact_name.png")


def test_search_book_by_partial_name(page, test_config):
    """
    TC-04b: Tìm sách bằng từ khóa một phần
    Input    : "Flutter"
    Expected : Hiển thị sách có chứa "Flutter"
    """
    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(page, SEARCH_PLACEHOLDER, "Flutter")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    sem_text = get_sem_text(page)
    assert (
        "Flutter" in sem_text
    ), f"Không tìm thấy sách chứa 'Flutter'.\nSem text (500 ký tự đầu): {sem_text[:500]}"

    page.screenshot(
        path=f"{test_config['screenshot_dir']}/tc04b_search_partial_name.png"
    )


def test_search_book_case_insensitive(page, test_config):
    """
    TC-04c: Tìm kiếm không phân biệt hoa/thường (REQ-03)
    Input    : "lập trình flutter" (viết thường)
    Expected : Vẫn tìm thấy "Lập trình Flutter cơ bản"
    """
    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(page, SEARCH_PLACEHOLDER, "lập trình flutter")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    sem_text = get_sem_text(page)
    assert "Flutter" in sem_text, "Tìm kiếm phân biệt hoa/thường — vi phạm REQ-03"

    page.screenshot(
        path=f"{test_config['screenshot_dir']}/tc04c_search_case_insensitive.png"
    )


def test_search_book_no_result(page, test_config):
    """
    TC-05: Tìm sách không có kết quả
    Input    : "xyzkhongtontai999"
    Expected : Hiển thị "Không tìm thấy sách"
    """
    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(page, SEARCH_PLACEHOLDER, "xyzkhongtontai999")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    sem_text = get_sem_text(page)
    assert (
        "Không tìm thấy sách" in sem_text
    ), f"Không hiển thị thông báo lỗi.\nSem text (500 ký tự đầu): {sem_text[:500]}"

    page.screenshot(path=f"{test_config['screenshot_dir']}/tc05_search_no_result.png")


def test_search_clear_shows_all_books(page, test_config):
    """
    TC-04d: Xóa từ khóa → danh sách trở về đầy đủ
    Input    : Nhập "Flutter" → reload trang → đăng nhập lại
    Expected : Hiển thị lại toàn bộ sách (không còn filter)
    """
    login(page, test_config)
    enable_flutter_semantics(page)

    # Tìm trước
    flutter_fill(page, SEARCH_PLACEHOLDER, "Flutter")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # Xác nhận đang có kết quả tìm kiếm
    sem_text_filtered = get_sem_text(page)
    assert "Flutter" in sem_text_filtered, "Bước setup: tìm kiếm không hoạt động"

    # Reload → về trang login → đăng nhập lại
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    # Đăng nhập lại
    login(page, test_config)
    enable_flutter_semantics(page)
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    sem_text = get_sem_text(page)
    assert (
        "Cấu trúc dữ liệu và giải thuật" in sem_text
    ), "Sau khi đăng nhập lại, danh sách không hiển thị đầy đủ sách"

    page.screenshot(path=f"{test_config['screenshot_dir']}/tc04d_search_clear.png")
