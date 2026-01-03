document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('update-modal');
    const form = document.getElementById('update-form');
    const cancelBtn = document.getElementById('cancel-btn');

    document.querySelectorAll('.open-modal-btn').forEach(button => {
        button.addEventListener('click', () => {
            // Get base URL for updating food
            let url = button.dataset.url;

            // Get selected date from data attributes
            const year = button.dataset.year;
            const month = button.dataset.month;
            const day = button.dataset.day;

            // Append query params for selected date
            url += `?year=${year}&month=${month}&day=${day}`;

            // Set form action dynamically
            form.action = url;

            // Show modal
            modal.classList.remove('hidden');
        });
    });

    // Cancel button
    cancelBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    // Optional: click outside modal to close
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    });
});
