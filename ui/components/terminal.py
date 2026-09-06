import streamlit as st


def render_terminal(
    stdout: str,
    stderr: str,
) -> None:
    """
    Render command output.
    """

    if stdout:

        st.subheader(
            "Output"
        )

        st.code(
            stdout,
            language="text",
        )

    else:

        st.info(
            "The command produced no standard output."
        )

    if stderr:

        st.subheader(
            "Error / Diagnostics"
        )

        st.code(
            stderr,
            language="text",
        )