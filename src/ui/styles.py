CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Space+Grotesk:wght@400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined');

    :root {
        --ember: #B8420A;
        --slate: #2F4550;
        --gold: #D98A1F;
        --ink: #2A2420;
        --mist: #6E655A;
        --cream: #F7F1E8;
        --cream-deep: #EFE4D3;
    }

    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--ink);
    }


    .main .block-container {
        max-width: 860px;
        padding-top: 2rem;
    }

    .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        vertical-align: middle;
        font-size: 1.2em;
    }

    .app-header {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.2rem;
    }

    .app-header h1 {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 1.9rem;
        margin: 0;
        color: var(--ink);
    }

    .app-header .material-symbols-outlined {
        font-size: 1.6rem;
        color: var(--ember);
    }

    .app-subtitle {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--mist);
        font-size: 0.92rem;
        margin-bottom: 1.5rem;
    }

    .tool-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.25rem 0.65rem;
        margin: 0.15rem 0.3rem 0.15rem 0;
        border-radius: 6px;
        font-size: 0.78rem;
        font-family: 'Space Grotesk', sans-serif;
        background: var(--ember);
        color: #FFF8EF;
        border: 1px solid var(--ember);
    }

    .tool-badge .material-symbols-outlined {
        font-size: 0.95rem;
        color: #FFF8EF;
    }

    .sidebar-section-title {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        color: var(--slate);
        display: flex;
        align-items: center;
        gap: 0.35rem;
        margin-bottom: 0.3rem;
    }

    .tool-list-item {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin: 0.35rem 0;
        font-size: 0.9rem;
        color: var(--ink);
    }

    .tool-list-item .material-symbols-outlined {
        font-size: 1.1rem;
        color: var(--gold);
    }

    .tool-list-item code {
        background: rgba(47, 69, 80, 0.08);
        padding: 0.1rem 0.35rem;
        border-radius: 4px;
    }

    .stChatMessage {
        border-radius: 10px;
    }

    button[kind="secondary"], .stButton button {
        border-radius: 6px !important;
        border: 1px solid var(--slate) !important;
        color: var(--slate) !important;
        background: transparent !important;
    }

    .stButton button:hover {
        background: var(--slate) !important;
        color: var(--cream) !important;
    }
</style>
"""