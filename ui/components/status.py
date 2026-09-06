import streamlit as st

from core.jobs import JobStatus


def render_status(
    status: JobStatus,
) -> None:

    if status == JobStatus.COMPLETED:

        st.success(
            f"Status: {status.value}"
        )

    elif status == JobStatus.FAILED:

        st.error(
            f"Status: {status.value}"
        )

    elif status == JobStatus.RUNNING:

        st.info(
            f"Status: {status.value}"
        )

    elif status == JobStatus.CANCELLED:

        st.warning(
            f"Status: {status.value}"
        )

    elif status == JobStatus.QUEUED:

        st.info(
            f"Status: {status.value}"
        )

    else:

        st.write(
            f"Status: {status.value}"
        )