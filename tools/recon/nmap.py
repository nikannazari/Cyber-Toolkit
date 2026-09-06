from typing import Any

from core.exceptions import ToolValidationError
from core.option import ToolOption
from core.parsers import (
    NmapParseResult,
    NmapParser,
)
from core.tool import Tool
from core.validators import (
    require_binary,
    require_non_empty,
    validate_ports,
)


class NmapTool(Tool):
    """
    Nmap integration for CyberToolkit.
    """

    name = "nmap"

    description = (
        "Network discovery and security auditing tool."
    )

    category = "recon"

    binary = "nmap"

    version = "unknown"

    def is_available(self) -> bool:
        """
        Check whether Nmap is installed.
        """

        try:

            require_binary(
                self.binary
            )

            return True

        except ToolValidationError:

            return False

    def options(self) -> list[ToolOption]:
        """
        Return options exposed by the UI.
        """

        return [

            ToolOption(
                name="target",
                label="Target",
                type="text",
                required=True,
                section="Basic",
                description=(
                    "IP address, hostname, or an "
                    "authorized laboratory target."
                ),
                placeholder="192.168.56.101",
            ),

            ToolOption(
                name="scan_type",
                label="Scan Type",
                type="select",
                choices=[
                    "TCP Connect",
                    "SYN",
                ],
                default="TCP Connect",
                section="Basic",
                description=(
                    "Choose the TCP scan technique."
                ),
            ),

            ToolOption(
                name="ports",
                label="Ports",
                type="text",
                required=False,
                section="Basic",
                description=(
                    "Optional port specification."
                ),
                placeholder="22,80,443",
            ),

            ToolOption(
                name="service_detection",
                label="Service Detection",
                type="boolean",
                default=False,
                section="Advanced",
                advanced=True,
                description=(
                    "Detect service and version "
                    "information (-sV)."
                ),
            ),

            ToolOption(
                name="os_detection",
                label="OS Detection",
                type="boolean",
                default=False,
                section="Advanced",
                advanced=True,
                description=(
                    "Attempt operating system "
                    "detection (-O)."
                ),
            ),

            ToolOption(
                name="timing",
                label="Timing",
                type="select",
                choices=[
                    "T2",
                    "T3",
                    "T4",
                    "T5",
                ],
                default="T3",
                section="Advanced",
                advanced=True,
                description=(
                    "Nmap timing template."
                ),
            ),

            ToolOption(
                name="verbosity",
                label="Verbosity",
                type="select",
                choices=[
                    "Normal",
                    "Verbose",
                    "Very Verbose",
                ],
                default="Normal",
                section="Advanced",
                advanced=True,
                description=(
                    "Control the amount of information "
                    "printed by Nmap."
                ),
            ),
        ]

    def validate(
        self,
        options: dict[str, Any],
    ) -> None:
        """
        Validate Nmap options.
        """

        target = options.get(
            "target"
        )

        require_non_empty(
            target,
            "target",
        )

        scan_type = options.get(
            "scan_type",
            "TCP Connect",
        )

        allowed_scan_types = {
            "TCP Connect",
            "SYN",
        }

        if scan_type not in allowed_scan_types:

            raise ToolValidationError(
                f"Unsupported scan type: {scan_type}"
            )

        ports = options.get(
            "ports"
        )

        if ports:

            validate_ports(
                ports
            )

        service_detection = options.get(
            "service_detection",
            False,
        )

        if not isinstance(
            service_detection,
            bool,
        ):

            raise ToolValidationError(
                "service_detection must be a boolean."
            )

        os_detection = options.get(
            "os_detection",
            False,
        )

        if not isinstance(
            os_detection,
            bool,
        ):

            raise ToolValidationError(
                "os_detection must be a boolean."
            )

        timing = options.get(
            "timing",
            "T3",
        )

        if timing not in {
            "T2",
            "T3",
            "T4",
            "T5",
        }:

            raise ToolValidationError(
                f"Unsupported timing template: {timing}"
            )

        verbosity = options.get(
            "verbosity",
            "Normal",
        )

        if verbosity not in {
            "Normal",
            "Verbose",
            "Very Verbose",
        }:

            raise ToolValidationError(
                f"Unsupported verbosity: {verbosity}"
            )

    def build_command(
        self,
        options: dict[str, Any],
    ) -> list[str]:
        """
        Build the Nmap argv list.
        """

        self.validate(
            options
        )

        command = [
            self.binary
        ]

        scan_type = options.get(
            "scan_type",
            "TCP Connect",
        )

        if scan_type == "TCP Connect":

            command.append(
                "-sT"
            )

        elif scan_type == "SYN":

            command.append(
                "-sS"
            )

        ports = options.get(
            "ports"
        )

        if ports:

            command.extend([
                "-p",
                ports.strip(),
            ])

        if options.get(
            "service_detection",
            False,
        ):

            command.append(
                "-sV"
            )

        if options.get(
            "os_detection",
            False,
        ):

            command.append(
                "-O"
            )

        timing = options.get(
            "timing",
            "T3",
        )

        command.append(
            f"-{timing}"
        )

        verbosity = options.get(
            "verbosity",
            "Normal",
        )

        if verbosity == "Verbose":

            command.append(
                "-v"
            )

        elif verbosity == "Very Verbose":

            command.append(
                "-vv"
            )

        target = options[
            "target"
        ].strip()

        command.append(
            target
        )

        return command

    def parse_output(
        self,
        output: str,
    ) -> NmapParseResult:
        """
        Parse Nmap stdout.
        """

        parser = NmapParser()

        return parser.parse(
            output
        )