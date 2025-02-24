document.getElementById("showLoginForm").addEventListener("click", function() {
    document.getElementById("main-container").style.display = "none"; // Ховаємо головне меню
    document.getElementById("loginForm").style.display = "block"; // Показуємо форму входу
});

document.getElementById("showRegisterForm").addEventListener("click", function() {
    document.getElementById("main-container").style.display = "none"; // Ховаємо головне меню
    document.getElementById("registerForm").style.display = "block"; // Показуємо форму реєстрації
});

document.getElementById("backToMain1").addEventListener("click", function() {
    document.getElementById("loginForm").style.display = "none"; // Ховаємо форму входу
    document.getElementById("main-container").style.display = "block"; // Повертаємо головне меню
});

document.getElementById("backToMain2").addEventListener("click", function() {
    document.getElementById("registerForm").style.display = "none"; // Ховаємо форму реєстрації
    document.getElementById("main-container").style.display = "block"; // Повертаємо головне меню
});
