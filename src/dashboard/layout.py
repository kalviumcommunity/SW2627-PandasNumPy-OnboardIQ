import streamlit as st

from src.config.settings import APP_NAME, VERSION


def configure_page() -> None:
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_header(
    title: str,
    subtitle: str | None = None,
) -> None:
    """Render a reusable page header."""
    st.title(title)

    if subtitle:
        st.caption(subtitle)


def render_sidebar_footer() -> None:
    """Render application information in the sidebar."""
    st.sidebar.divider()

    st.sidebar.caption(f"{APP_NAME}")
    st.sidebar.caption(f"Version {VERSION}")


def render_metric_cards(metrics: list[dict[str, str]]) -> None:
    """
    Render reusable metric cards.

    Each metric dictionary should contain:
    - label
    - value
    - optional help
    """
    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics):
        with column:
            help_text = metric.get("help")

            st.metric(
                label=metric["label"],
                value=metric["value"],
                help=help_text,
            )


def render_empty_state(
    title: str,
    message: str,
) -> None:
    """Render a reusable empty-state message."""
    st.info(f"**{title}**\n\n{message}")