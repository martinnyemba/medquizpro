/**
 * MedQuizPro Navigation System
 * Enhanced version with better mobile support and performance optimizations
 */
class NavigationSystem {
    constructor() {
        this.init();
        this.setupDropdowns();
        this.setupMobileMenu();
        this.setupTouchEvents();
        this.setupKeyboardNav();
        this.setupSearch();
        this.setupScrollBehavior();
        this.setupResizeHandler();
    }

    init() {
        // Cache DOM elements
        this.navbar = document.querySelector('.navbar');
        this.hamburger = document.querySelector('.hamburger');
        this.navLinks = document.querySelector('.nav-links');
        this.dropdowns = document.querySelectorAll('.nav-dropdown');
        this.searchBar = document.querySelector('.search-bar');
        this.searchTrigger = document.querySelector('[data-search-trigger]');
        this.searchClose = document.querySelector('[data-search-close]');
        this.searchInput = document.querySelector('.search-input');
        this.searchResults = document.querySelector('.search-results');

        // State management
        this.isNavOpen = false;
        this.currentDropdown = null;
        this.isSearchOpen = false;
        this.isMobile = window.innerWidth <= 768;
        this.lastScrollTop = 0;
        this.resizeTimeout = null;

        // Initialize viewport-specific behaviors
        this.handleViewportSpecificBehaviors();
    }

    setupResizeHandler() {
        window.addEventListener('resize', () => {
            if (this.resizeTimeout) {
                clearTimeout(this.resizeTimeout);
            }

            this.resizeTimeout = setTimeout(() => {
                const wasMobile = this.isMobile;
                this.isMobile = window.innerWidth <= 768;

                if (wasMobile !== this.isMobile) {
                    this.handleViewportChange();
                }
            }, 250);
        });
    }

    handleViewportChange() {
        this.resetNavigation();
        this.handleViewportSpecificBehaviors();
    }

    handleViewportSpecificBehaviors() {
        if (this.isMobile) {
            this.setupMobileSpecificBehaviors();
        } else {
            this.setupDesktopSpecificBehaviors();
        }
    }

    setupMobileSpecificBehaviors() {
        // Add mobile-specific event listeners and behaviors
        document.body.addEventListener('touchmove', this.handleMobileScroll.bind(this), { passive: false });
    }

    setupDesktopSpecificBehaviors() {
        // Remove mobile-specific listeners and reset states
        document.body.removeEventListener('touchmove', this.handleMobileScroll);
        this.resetNavigation();
    }

    handleMobileScroll(e) {
        if (this.isNavOpen) {
            e.preventDefault();
        }
    }

    resetNavigation() {
        this.isNavOpen = false;
        this.currentDropdown = null;

        if (this.hamburger) {
            this.hamburger.classList.remove('active');
            this.hamburger.setAttribute('aria-expanded', 'false');
        }

        if (this.navLinks) {
            this.navLinks.classList.remove('active');
        }

        document.body.style.overflow = '';
        this.closeAllDropdowns();
    }

    setupDropdowns() {
        this.dropdowns.forEach(dropdown => {
            const button = dropdown.querySelector('.nav-dropdown-btn');
            const content = dropdown.querySelector('.nav-dropdown-content');

            if (!button || !content) return;

            button.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                this.toggleDropdown(dropdown);
            });

            // Enhanced keyboard navigation
            this.setupDropdownKeyboardNav(dropdown);
        });

        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.nav-dropdown')) {
                this.closeAllDropdowns();
            }
        });
    }

    setupDropdownKeyboardNav(dropdown) {
        const content = dropdown.querySelector('.nav-dropdown-content');
        const items = content.querySelectorAll('a[role="menuitem"]');

        content.addEventListener('keydown', (e) => {
            const currentIndex = Array.from(items).indexOf(document.activeElement);

            switch (e.key) {
                case 'ArrowUp':
                    e.preventDefault();
                    if (currentIndex > 0) {
                        items[currentIndex - 1].focus();
                    } else {
                        items[items.length - 1].focus();
                    }
                    break;

                case 'ArrowDown':
                    e.preventDefault();
                    if (currentIndex < items.length - 1) {
                        items[currentIndex + 1].focus();
                    } else {
                        items[0].focus();
                    }
                    break;

                case 'Home':
                    e.preventDefault();
                    items[0].focus();
                    break;

                case 'End':
                    e.preventDefault();
                    items[items.length - 1].focus();
                    break;

                case 'Escape':
                    e.preventDefault();
                    this.closeDropdown(dropdown);
                    dropdown.querySelector('.nav-dropdown-btn').focus();
                    break;

                case 'Tab':
                    if (currentIndex === items.length - 1 && !e.shiftKey) {
                        this.closeDropdown(dropdown);
                    }
                    break;
            }
        });
    }

    toggleDropdown(dropdown) {
        const button = dropdown.querySelector('.nav-dropdown-btn');
        const content = dropdown.querySelector('.nav-dropdown-content');
        const isExpanded = content.classList.contains('active');

        // Close other dropdowns
        if (this.currentDropdown && this.currentDropdown !== dropdown) {
            this.closeDropdown(this.currentDropdown);
        }

        // Toggle current dropdown
        button.setAttribute('aria-expanded', !isExpanded);
        content.classList.toggle('active');

        if (!isExpanded) {
            // Focus first menu item when opening
            requestAnimationFrame(() => {
                content.querySelector('[role="menuitem"]')?.focus();
            });
        }

        this.currentDropdown = isExpanded ? null : dropdown;
    }

    closeDropdown(dropdown) {
        const button = dropdown.querySelector('.nav-dropdown-btn');
        const content = dropdown.querySelector('.nav-dropdown-content');

        button.setAttribute('aria-expanded', 'false');
        content.classList.remove('active');
    }

    closeAllDropdowns() {
        this.dropdowns.forEach(dropdown => this.closeDropdown(dropdown));
        this.currentDropdown = null;
    }

    setupMobileMenu() {
        if (!this.hamburger || !this.navLinks) return;

        this.hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleMobileMenu();
        });
    }

    toggleMobileMenu() {
        this.isNavOpen = !this.isNavOpen;

        this.hamburger.classList.toggle('active');
        this.navLinks.classList.toggle('active');
        this.hamburger.setAttribute('aria-expanded', this.isNavOpen);

        // Handle body scroll
        document.body.style.overflow = this.isNavOpen ? 'hidden' : '';

        // Close dropdowns when closing menu
        if (!this.isNavOpen) {
            this.closeAllDropdowns();
        }
    }

    setupTouchEvents() {
        if ('ontouchstart' in window) {
            this.dropdowns.forEach(dropdown => {
                const content = dropdown.querySelector('.nav-dropdown-content');
                let touchStartY = 0;
                let touchEndY = 0;

                content.addEventListener('touchstart', (e) => {
                    touchStartY = e.touches[0].clientY;
                }, { passive: true });

                content.addEventListener('touchmove', (e) => {
                    touchEndY = e.touches[0].clientY;
                    const deltaY = touchEndY - touchStartY;
                    const isAtTop = content.scrollTop === 0;
                    const isAtBottom = content.scrollTop + content.clientHeight >= content.scrollHeight;

                    // Prevent default only when needed
                    if ((isAtTop && deltaY > 0) || (isAtBottom && deltaY < 0)) {
                        e.preventDefault();
                    }
                }, { passive: false });
            });
        }
    }

    setupSearch() {
        if (!this.searchTrigger || !this.searchClose || !this.searchBar) return;

        this.searchTrigger.addEventListener('click', () => this.toggleSearch(true));
        this.searchClose.addEventListener('click', () => this.toggleSearch(false));

        // Handle search input with debounce
        let searchTimeout;
        this.searchInput?.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.handleSearch(e.target.value);
            }, 300);
        });

        // Close search with Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isSearchOpen) {
                this.toggleSearch(false);
            }
        });

        // Close search when clicking outside
        document.addEventListener('click', (e) => {
            if (this.isSearchOpen &&
                !this.searchBar.contains(e.target) &&
                !this.searchTrigger.contains(e.target)) {
                this.toggleSearch(false);
            }
        });
    }

    toggleSearch(isOpen) {
        this.isSearchOpen = isOpen;
        this.searchBar.classList.toggle('search-bar-open', isOpen);

        if (isOpen) {
            this.searchInput?.focus();
            document.body.style.overflow = 'hidden';
        } else {
            if (this.searchInput) this.searchInput.value = '';
            this.clearSearchResults();
            document.body.style.overflow = '';
        }

        this.searchTrigger?.setAttribute('aria-expanded', isOpen);
        this.searchBar.setAttribute('aria-hidden', !isOpen);
    }

    handleSearch(query) {
        if (!query.trim()) {
            this.clearSearchResults();
            return;
        }

        // Example search implementation
        const searchResults = [
            { title: `Result for "${query}"`, url: '#' },
            { title: `Another result for "${query}"`, url: '#' },
            { title: `More results for "${query}"`, url: '#' }
        ];

        this.updateSearchResults(searchResults);
    }

    updateSearchResults(results) {
        if (!this.searchResults) return;

        this.searchResults.innerHTML = results.map(result => `
            <li class="search-result-item">
                <a href="${result.url}" class="search-result-link">
                    <span class="search-result-text">${result.title}</span>
                </a>
            </li>
        `).join('');

        this.searchResults.classList.toggle('has-results', results.length > 0);
    }

    clearSearchResults() {
        if (!this.searchResults) return;

        this.searchResults.innerHTML = '';
        this.searchResults.classList.remove('has-results');
    }

    setupScrollBehavior() {
        let scrollTimeout;
        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            if (scrollTimeout) {
                window.cancelAnimationFrame(scrollTimeout);
            }

            scrollTimeout = window.requestAnimationFrame(() => {
                const currentScroll = window.pageYOffset;

                // Don't hide navbar when mobile menu is open
                if (!this.isNavOpen) {
                    if (currentScroll > lastScroll && currentScroll > 100) {
                        // Scrolling down - hide navbar
                        this.navbar.classList.add('nav-hidden');
                    } else {
                        // Scrolling up - show navbar
                        this.navbar.classList.remove('nav-hidden');
                    }
                }

                lastScroll = currentScroll;
            });
        }, { passive: true });
    }

    setupKeyboardNav() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (this.currentDropdown) {
                    this.closeAllDropdowns();
                } else if (this.isNavOpen) {
                    this.toggleMobileMenu();
                }
            }
        });
    }
}

// Initialize the navigation system when the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new NavigationSystem();

    // Initialize Bootstrap tooltips if present
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers if present
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});