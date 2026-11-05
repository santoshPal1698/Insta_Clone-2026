document.addEventListener("DOMContentLoaded", function () {
    var passwordFields = document.querySelectorAll(".auth-form input[type='password']");

    passwordFields.forEach(function (input) {
        var wrapper = document.createElement("div");
        wrapper.className = "auth-password-wrap";
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        var toggle = document.createElement("button");
        toggle.className = "auth-password-toggle";
        toggle.type = "button";
        toggle.setAttribute("aria-label", "Show password");
        toggle.setAttribute("aria-pressed", "false");
        toggle.innerHTML =
            '<svg class="auth-eye-open" viewBox="0 0 24 24" aria-hidden="true">' +
            '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"></path>' +
            '<circle cx="12" cy="12" r="3"></circle>' +
            "</svg>" +
            '<svg class="auth-eye-closed" viewBox="0 0 24 24" aria-hidden="true">' +
            '<path d="m3 3 18 18M10.6 10.6a2 2 0 0 0 2.8 2.8"></path>' +
            '<path d="M9.9 5.2A10.7 10.7 0 0 1 12 5c6.4 0 10 7 10 7a15.7 15.7 0 0 1-3.1 3.8M6.2 6.2C3.5 8 2 12 2 12s3.6 7 10 7c1.2 0 2.3-.3 3.3-.7"></path>' +
            "</svg>";

        toggle.addEventListener("click", function () {
            var isVisible = input.type === "text";
            input.type = isVisible ? "password" : "text";
            toggle.setAttribute("aria-label", isVisible ? "Show password" : "Hide password");
            toggle.setAttribute("aria-pressed", String(!isVisible));
            wrapper.classList.toggle("is-visible", !isVisible);
        });

        wrapper.appendChild(toggle);
    });

});
