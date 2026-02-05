(function() {
    function removeTriangles() {
        // Find all elements in the sidebar with option-menu classes
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) return;
        
        // Find option menu container
        const optionMenus = sidebar.querySelectorAll('[class*="option-menu"]');
        optionMenus.forEach(menu => {
            // Remove all ::before and ::after pseudo-elements
            const style = document.createElement('style');
            style.textContent = `
                [class*="option-menu"]::before,
                [class*="option-menu"]::after,
                [class*="option-menu"] *::before,
                [class*="option-menu"] *::after {
                    display: none !important;
                    content: none !important;
                    visibility: hidden !important;
                }
            `;
            document.head.appendChild(style);
            
            // Remove any absolutely positioned small elements (likely triangles)
            const allElements = menu.querySelectorAll('*');
            allElements.forEach(el => {
                const style = window.getComputedStyle(el);
                if ((style.position === 'absolute' || style.position === 'fixed') &&
                    (parseInt(style.width) < 20 || parseInt(style.height) < 20)) {
                    el.style.display = 'none';
                }
            });
        });
    }
    
    // Run immediately and also after a short delay
    removeTriangles();
    setTimeout(removeTriangles, 100);
    setTimeout(removeTriangles, 500);
    
    // Also run when DOM changes
    const observer = new MutationObserver(removeTriangles);
    observer.observe(document.body, { childList: true, subtree: true });
})();
