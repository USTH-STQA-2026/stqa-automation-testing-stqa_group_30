import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    login,
    smart_fill,
    wait_for_flutter,
)
from web_detector import WebTech, detect_technology

SEARCH_PLACEHOLDER = "Tìm kiếm theo tên sách hoặc tác giả..."

def get_sem_text(page):
    """Lấy toàn bộ text + aria-label từ Semantics Tree."""
    elements = page.locator("flt-semantics").all()
    texts = []
    for el in elements:
        texts.append(el.inner_text() or "")
        texts.append(el.get_attribute("aria-label") or "")
    return " ".join(texts)

@pytest.mark.parametrize(
    "search_keyword, expected_text, error_message, tc_id",
    [
        (
            "Lập trình Flutter cơ bản", 
            "Lập trình Flutter cơ bản", 
            "Không tìm thấy sách bằng tên chính xác.", 
            "tc04a_search_exact_name"
        ),
        (
            "Flutter", 
            "Flutter", 
            "Không tìm thấy sách chứa từ khóa một phần.", 
            "tc04b_search_partial_name"
        ),
        (
            "lập trình flutter", 
            "Flutter", 
            "Tìm kiếm phân biệt hoa/thường — vi phạm REQ-03.", 
            "tc04c_search_case_insensitive"
        ),
        (
            "notexistingbook", 
            "Không tìm thấy sách", 
            "Không hiển thị thông báo lỗi khi không có kết quả.", 
            "tc05_search_no_result"
        ),
    ]
)
def test_search_book_behavior(page, test_config, search_keyword, expected_text, error_message, tc_id):
    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(page, SEARCH_PLACEHOLDER, search_keyword)
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    sem_text = get_sem_text(page)
    assert expected_text in sem_text, f"{error_message}\nSem text (500 ký tự đầu): {sem_text[:500]}"

    page.screenshot(path=f"{test_config['screenshot_dir']}/{tc_id}.png")

def test_search_clear_shows_all_books(page, test_config):
    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(page, SEARCH_PLACEHOLDER, "Flutter")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    sem_text_filtered = get_sem_text(page)
    assert "Flutter" in sem_text_filtered, "Bước setup: tìm kiếm không hoạt động"

    page.reload(wait_until="networkidle")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    login(page, test_config)
    enable_flutter_semantics(page)
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    sem_text = get_sem_text(page)
    assert "Cấu trúc dữ liệu và giải thuật" in sem_text, "Sau khi đăng nhập lại, danh sách không hiển thị đầy đủ sách"

    page.screenshot(path=f"{test_config['screenshot_dir']}/tc04d_search_clear.png")

@pytest.mark.parametrize(
    "filter_keyword",
    [
        "Công nghệ",
        "công nghệ",
    ]
)
def test_filter_books_by_category(page, test_config, web_tech, filter_keyword):
    login(page, test_config)
    
    FILTER_INPUT_LABEL = "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)" 

    smart_fill(page, label=FILTER_INPUT_LABEL, value=filter_keyword, tech=web_tech)
    
    page.wait_for_timeout(1500) 
    if web_tech.is_flutter_canvaskit:
        enable_flutter_semantics(page)

    sem_text = get_sem_text(page) if web_tech.is_flutter_canvaskit else page.content()
    assert filter_keyword in sem_text, f"Error: Cant find valid '{filter_keyword}'."

    page.screenshot(path=f"{test_config['screenshot_dir']}/input_filter_{filter_keyword}.png")