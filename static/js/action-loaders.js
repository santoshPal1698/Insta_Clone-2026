(function () {
    function loadingMessage(element) {
        var customMessage = element.getAttribute("data-loading-text");
        if (customMessage) {
            return customMessage;
        }

        var label = (element.textContent || element.value || "").trim().toLowerCase();
        if (label.indexOf("search") !== -1) return "Searching...";
        if (label.indexOf("login") !== -1 || label.indexOf("log in") !== -1) return "Signing in...";
        if (label.indexOf("register") !== -1 || label.indexOf("create account") !== -1) {
            return "Creating your account...";
        }
        if (label.indexOf("delete") !== -1 || label.indexOf("remove") !== -1) return "Deleting...";
        if (label.indexOf("send") !== -1 || label.indexOf("comment") !== -1 || label.indexOf("reply") !== -1) {
            return "Sending...";
        }
        if (label.indexOf("save") !== -1 || label.indexOf("publish") !== -1 || label.indexOf("update") !== -1) {
            return "Saving..";
        }
        return "Please wait..";
    }

    function startLoading(element) {
        if (element.dataset.actionLoading === "true") {
            return;
        }

        var messageText = loadingMessage(element);
        element.dataset.actionLoading = "true";
        element.setAttribute("aria-busy", "true");

        if (element.classList.contains("auth-submit")) {
            element.classList.add("is-loading");
            return;
        }

        if (element instanceof HTMLInputElement) {
            element.dataset.actionOriginalValue = element.value;
            element.value = messageText;
            element.classList.add("is-action-loading");
            return;
        }

        Array.from(element.childNodes).forEach(function (child) {
            if (child.nodeType === Node.TEXT_NODE && child.textContent.trim()) {
                var content = document.createElement("span");
                content.className = "action-button-content";
                child.parentNode.replaceChild(content, child);
                content.appendChild(child);
            }
        });

        var loading = document.createElement("span");
        loading.className = "action-button-loading";
        loading.setAttribute("role", "status");
        loading.setAttribute("aria-live", "polite");

        var spinner = document.createElement("span");
        spinner.className = "action-button-spinner";
        spinner.setAttribute("aria-hidden", "true");

        var message = document.createElement("span");
        message.textContent = messageText;

        loading.appendChild(spinner);
        loading.appendChild(message);
        element.appendChild(loading);
        element.classList.add("is-action-loading");
    }

    function stopLoading(element) {
        element.classList.remove("is-action-loading", "is-loading");
        element.removeAttribute("aria-busy");
        delete element.dataset.actionLoading;

        if (element instanceof HTMLInputElement && element.dataset.actionOriginalValue) {
            element.value = element.dataset.actionOriginalValue;
            delete element.dataset.actionOriginalValue;
        }

        var loading = element.querySelector(":scope > .action-button-loading");
        if (loading) {
            loading.remove();
        }

        var content = element.querySelector(":scope > .action-button-content");
        if (content) {
            while (content.firstChild) {
                content.parentNode.insertBefore(content.firstChild, content);
            }
            content.remove();
        }

        if (element.form) {
            delete element.form.dataset.actionLoading;
        }
    }

    document.addEventListener(
        "submit",
        function (event) {
            var form = event.target;
            if (!(form instanceof HTMLFormElement) || form.dataset.actionLoading === "true") {
                if (form instanceof HTMLFormElement) {
                    event.preventDefault();
                }
                return;
            }

            var submitter = event.submitter;
            if (!submitter) {
                submitter = form.querySelector("button[type='submit'], button:not([type]), input[type='submit']");
            }

            if (submitter && submitter.getAttribute("data-no-loader") !== null) {
                return;
            }

            form.dataset.actionLoading = "true";
            if (submitter) {
                startLoading(submitter);
            }
        },
        true
    );

    document.addEventListener(
        "click",
        function (event) {
            var target = event.target instanceof Element ? event.target : event.target.parentElement;
            if (!target) {
                return;
            }

            var link = target.closest(
                "a.btn[href], a.account-submit[href], a.account-link[href], " +
                "a.feed-create[href], a.feed-action[href], a.social-detail-edit[href], " +
                "a.social-detail-like[href], a.social-detail-back[href], " +
                "a.social-person-view-btn[href], a.social-person-follow-btn[href], " +
                "a.social-person-following-btn[href], a.social-profile-edit-btn[href], " +
                "a.social-profile-posts-btn[href], a.social-profile-save-btn[href], " +
                "a.social-profile-cancel-btn[href], a.social-delete-cancel[href], " +
                "a.site-logout[href], a[data-action-loader][href], a[data-loading-text][href]"
            );

            if (
                !link ||
                event.button !== 0 ||
                event.metaKey ||
                event.ctrlKey ||
                event.shiftKey ||
                event.altKey ||
                link.target === "_blank" ||
                link.hasAttribute("download") ||
                link.hasAttribute("data-toggle") ||
                link.hasAttribute("data-no-loader") ||
                link.getAttribute("href").charAt(0) === "#"
            ) {
                return;
            }

            var destination = new URL(link.href, window.location.href);
            if (destination.origin !== window.location.origin) {
                return;
            }

            startLoading(link);
        },
        true
    );

    if (window.jQuery) {
        window.jQuery(document).on("ajaxError.actionLoaders", function () {
            document
                .querySelectorAll(".is-action-loading, .auth-submit.is-loading")
                .forEach(stopLoading);
        });
    }
})();
