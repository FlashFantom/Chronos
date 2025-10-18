# Modern UI Styles for Chronos

MODERN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
        min-height: 100vh;
        transition: all 0.3s ease;
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 2rem;
    }
    
    /* Modern buttons */
    .q-btn {
        border-radius: 16px !important;
        text-transform: none !important;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .q-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .q-btn:active {
        transform: translateY(0);
    }
    
    /* Toggle buttons */
    .q-btn-toggle {
        border-radius: 20px !important;
        overflow: hidden;
    }
    
    .q-btn-toggle .q-btn {
        font-size: 1.2rem !important;
        padding: 1rem 2rem !important;
        min-height: 60px;
    }
    
    /* Info cards */
    .info-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Welcome text */
    .welcome-text {
        color: white;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Timer display */
    .timer-display {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 2rem;
    }
    
    /* Login card */
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        min-width: 400px;
    }
    
    /* Input fields */
    .q-field__control {
        border-radius: 12px !important;
    }
    
    /* End day button */
    .end-day-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        font-weight: 600;
    }
    
    /* Admin button */
    .admin-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Seasonal decorations */
    .seasonal-icon {
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
        transition: all 0.3s ease;
    }
    
    .seasonal-icon:hover {
        filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.3));
        transform: rotate(360deg) scale(1.1);
    }
    
    /* Table styling */
    .q-table {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        overflow: hidden;
    }
    
    .q-table thead tr {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .q-table tbody tr:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Smooth transitions */
    * {
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    
    /* Break mode styling */
    body.break-mode {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* Busy mode styling */
    body.busy-mode {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    /* Pulse animation */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Success animation */
    @keyframes successBounce {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    .success-bounce {
        animation: successBounce 0.5s ease-in-out;
    }
</style>
"""

