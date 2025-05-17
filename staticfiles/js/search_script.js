// Custom script for search tab switching
document.addEventListener('DOMContentLoaded', function() {
    // Get all search tabs
    const searchTabs = document.querySelectorAll('.search_tab');
    // Get all search panels
    const searchPanels = document.querySelectorAll('.search_panel');
    
    // Add click event to each tab
    searchTabs.forEach((tab, index) => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs and panels
            searchTabs.forEach(t => t.classList.remove('active'));
            searchPanels.forEach(p => p.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding panel
            tab.classList.add('active');
            searchPanels[index].classList.add('active');
        });
    });
    
    // Date picker initialization (if you're using a library like flatpickr or bootstrap-datepicker)
    // This is just a placeholder - you might need to adjust based on your actual date picker library
    if (typeof flatpickr !== 'undefined') {
        flatpickr('.check_in', {
            minDate: "today",
            dateFormat: "Y-m-d"
        });
        
        flatpickr('.check_out', {
            minDate: "today",
            dateFormat: "Y-m-d"
        });
    }
});