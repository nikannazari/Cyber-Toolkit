import shlex

import streamlit as st

from core import Executor, JobManager
from core.jobs import JobStatus
from core.registry import ToolRegistry

from ui.components.status import render_status
from ui.components.terminal import render_terminal
from ui.tool_form import render_tool_form


def render_dashboard(
    registry: ToolRegistry,
    executor: Executor,
    job_manager: JobManager,
    selected_tool: str | None,
) -> None:

    st.title(
        "🛡️ CyberToolkit"
    )

    st.write(
        "Modular security toolkit framework."
    )

    st.divider()

    if selected_tool is None:

        render_home(
            registry,
            job_manager,
        )

        return

    try:

        tool = registry.get(
            selected_tool
        )

    except Exception as exc:

        st.error(
            f"Unable to load tool: {exc}"
        )

        return

    render_tool_header(
        tool
    )

    if not tool.is_available():

        st.error(
            f"'{tool.binary}' was not found in PATH."
        )

        return

    st.success(
        "Tool is available."
    )

    st.divider()

    options = render_tool_form(
        tool
    )

    if options is None:
        return

    try:

        command = tool.build_command(
            options
        )

    except Exception as exc:

        st.error(
            f"Validation error: {exc}"
        )

        return

    st.divider()

    st.subheader(
        "Command Preview"
    )

    st.code(
        shlex.join(command),
        language="bash",
    )

    try:

        job = job_manager.create(
            tool_name=tool.name,
            command=command,
        )

        job_manager.update_status(
            job.id,
            JobStatus.RUNNING,
        )

        result = executor.run(
            command
        )

        job_manager.attach_result(
            job.id,
            result,
        )

        st.divider()

        render_status(
            job.status
        )

        render_execution_metrics(
            result.return_code,
            result.duration,
            job.id,
        )

        render_execution_details(
            job,
            result,
        )

        render_structured_result(
            tool,
            result.stdout,
        )

        render_terminal(
            result.stdout,
            result.stderr,
        )

    except Exception as exc:

        st.error(
            f"Execution error: {exc}"
        )


def render_tool_header(
    tool,
) -> None:

    st.header(
        tool.name
    )

    st.caption(
        tool.description
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.write(
            f"**Category:** {tool.category}"
        )

    with col2:

        st.write(
            f"**Binary:** `{tool.binary}`"
        )

    with col3:

        st.write(
            f"**Version:** `{tool.version}`"
        )


def render_execution_metrics(
    return_code: int,
    duration: float,
    job_id: str,
) -> None:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Return Code",
            return_code,
        )

    with col2:

        st.metric(
            "Duration",
            f"{duration:.3f}s",
        )

    with col3:

        st.metric(
            "Job",
            job_id[:8],
        )


def render_execution_details(
    job,
    result,
) -> None:

    with st.expander(
        "Execution Details",
        expanded=False,
    ):

        st.write(
            f"**Job ID:** `{job.id}`"
        )

        st.write(
            f"**Command:** "
            f"`{result.command_string}`"
        )

        st.write(
            f"**Started:** "
            f"`{result.started_at}`"
        )

        st.write(
            f"**Finished:** "
            f"`{result.finished_at}`"
        )


def render_structured_result(
    tool,
    stdout: str,
) -> None:

    if tool.name != "nmap":
        return

    parsed = tool.parse_output(
        stdout
    )

    st.subheader(
        "Scan Summary"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Hosts",
            parsed.host_count,
        )

    with col2:

        st.metric(
            "Ports",
            parsed.port_count,
        )

    if not parsed.hosts:

        st.info(
            "No hosts were parsed from the output."
        )

        return

    for host in parsed.hosts:

        hostname = (
            f" ({host.hostname})"
            if host.hostname
            else ""
        )

        with st.expander(
            f"{host.address}{hostname} — "
            f"{host.status}",
            expanded=True,
        ):

            if not host.ports:

                st.info(
                    "No ports were parsed."
                )

                continue

            table = []

            for port in host.ports:

                table.append(
                    {
                        "Port": port.port,
                        "Protocol": port.protocol,
                        "State": port.state,
                        "Service": port.service or "",
                        "Details": port.product or "",
                    }
                )

            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True,
            )


def render_home(
    registry: ToolRegistry,
    job_manager: JobManager,
) -> None:

    st.subheader(
        "Dashboard"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Registered Tools",
            registry.count(),
        )

    with col2:

        st.metric(
            "Jobs",
            len(job_manager.all()),
        )

    with col3:

        available = sum(
            tool.is_available()
            for tool in registry.all()
        )

        st.metric(
            "Available Tools",
            available,
        )

    st.divider()

    st.info(
        "Select a tool from the sidebar "
        "to configure and run it."
    )