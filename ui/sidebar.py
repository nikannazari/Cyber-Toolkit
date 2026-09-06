import streamlit as st

from core.registry import ToolRegistry


def render_sidebar(
    registry: ToolRegistry,
) -> str | None:

    st.sidebar.title(
        "🛡️ CyberToolkit"
    )

    st.sidebar.caption(
        "Security Toolkit Framework"
    )

    st.sidebar.divider()

    categories = registry.categories()

    if "selected_tool" not in st.session_state:

        st.session_state.selected_tool = None

    for category, tools in categories.items():

        st.sidebar.subheader(
            category.capitalize()
        )

        for tool in tools:

            available = tool.is_available()

            label = (
                f"🟢 {tool.name}"
                if available
                else f"🔴 {tool.name}"
            )

            if st.sidebar.button(
                label,
                key=f"tool_{tool.name}",
                use_container_width=True,
            ):

                st.session_state.selected_tool = (
                    tool.name
                )

    return st.session_state.selected_tool