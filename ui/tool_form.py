from typing import Any

import streamlit as st

from core.option import ToolOption
from core.tool import Tool


def render_tool_form(
    tool: Tool,
) -> dict[str, Any] | None:
    """
    Render a generic Streamlit form for a tool.

    Returns:
        Dictionary of user-provided values when submitted.
        None when the form has not been submitted.
    """

    options = tool.options()

    if not options:

        st.info(
            "This tool does not require any options."
        )

    values: dict[str, Any] = {}

    basic_options = [
        option
        for option in options
        if not option.advanced
    ]

    advanced_options = [
        option
        for option in options
        if option.advanced
    ]

    with st.form(
        key=f"tool_form_{tool.name}"
    ):

        if basic_options:

            st.subheader(
                "Basic Options"
            )

            for option in basic_options:

                if not option.visible:
                    continue

                values[option.name] = render_option(
                    option
                )

        if advanced_options:

            with st.expander(
                "Advanced Options",
                expanded=False,
            ):

                for option in advanced_options:

                    if not option.visible:
                        continue

                    values[option.name] = render_option(
                        option
                    )

        submitted = st.form_submit_button(
            "▶ Run",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        errors = validate_required_options(
            options,
            values,
        )

        if errors:

            for error in errors:
                st.error(error)

            return None

        return values

    return None


def validate_required_options(
    options: list[ToolOption],
    values: dict[str, Any],
) -> list[str]:
    """
    Validate generic required fields.
    """

    errors: list[str] = []

    for option in options:

        if not option.required:
            continue

        value = values.get(
            option.name
        )

        if value is None:

            errors.append(
                f"{option.label} is required."
            )

            continue

        if isinstance(value, str):

            if not value.strip():

                errors.append(
                    f"{option.label} is required."
                )

    return errors


def render_option(
    option: ToolOption,
) -> Any:

    if option.type == "text":

        return st.text_input(
            label=option.label,
            value=(
                option.default
                if option.default is not None
                else ""
            ),
            placeholder=option.placeholder,
            help=option.description,
        )

    if option.type == "textarea":

        return st.text_area(
            label=option.label,
            value=(
                option.default
                if option.default is not None
                else ""
            ),
            placeholder=option.placeholder,
            help=option.description,
        )

    if option.type == "boolean":

        return st.checkbox(
            label=option.label,
            value=(
                bool(option.default)
                if option.default is not None
                else False
            ),
            help=option.description,
        )

    if option.type == "select":

        if not option.choices:

            st.error(
                f"Option '{option.name}' "
                "has no available choices."
            )

            return None

        index = 0

        if option.default in option.choices:

            index = option.choices.index(
                option.default
            )

        return st.selectbox(
            label=option.label,
            options=option.choices,
            index=index,
            help=option.description,
        )

    if option.type == "integer":

        return st.number_input(
            label=option.label,
            min_value=(
                int(option.min_value)
                if option.min_value is not None
                else None
            ),
            max_value=(
                int(option.max_value)
                if option.max_value is not None
                else None
            ),
            value=(
                int(option.default)
                if option.default is not None
                else 0
            ),
            step=(
                int(option.step)
                if option.step is not None
                else 1
            ),
            help=option.description,
        )

    if option.type == "float":

        return st.number_input(
            label=option.label,
            min_value=(
                float(option.min_value)
                if option.min_value is not None
                else None
            ),
            max_value=(
                float(option.max_value)
                if option.max_value is not None
                else None
            ),
            value=(
                float(option.default)
                if option.default is not None
                else 0.0
            ),
            step=(
                float(option.step)
                if option.step is not None
                else 0.1
            ),
            help=option.description,
        )

    st.error(
        f"Unsupported option type: {option.type}"
    )

    return None