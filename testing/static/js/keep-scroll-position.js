document.addEventListener('DOMContentLoaded', function() {
    const testCaseList = document.querySelector('.created-test-cases');

    // Восстановление позиции скролла при загрузке страницы
    const scrollPosition = sessionStorage.getItem('scrollPosition');
    if (scrollPosition) {
        testCaseList.scrollTop = parseInt(scrollPosition, 10);
    }

    // Сохранение позиции скролла при клике на ссылку
    document.querySelectorAll('.test-case-link').forEach(link => {
        link.addEventListener('click', () => {
            sessionStorage.setItem('scrollPosition', testCaseList.scrollTop);
        });
    });
});
