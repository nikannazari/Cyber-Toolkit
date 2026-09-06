import streamlit as st

from core import Executor, JobManager
from tools import create_registry

from ui.dashboard import render_dashboard
from ui.sidebar import render_sidebar


st.set_page_config(
    page_title="CyberToolkit",
    page_icon="🛡️",
    layout="wide",
)


def initialize_state() -> None:
    """
    Initialize application-wide objects.
    """

    if "registry" not in st.session_state:

        st.session_state.registry = (
            create_registry()
        )

    if "executor" not in st.session_state:

        st.session_state.executor = Executor(
            default_timeout=300
        )

    if "job_manager" not in st.session_state:

        st.session_state.job_manager = (
            JobManager()
        )


initialize_state()


registry = (
    st.session_state.registry
)

executor = (
    st.session_state.executor
)

job_manager = (
    st.session_state.job_manager
)


selected_tool = render_sidebar(
    registry
)


render_dashboard(
    registry=registry,
    executor=executor,
    job_manager=job_manager,
    selected_tool=selected_tool,
)