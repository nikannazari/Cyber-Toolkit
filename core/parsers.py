import re
from dataclasses import dataclass, field


@dataclass
class PortResult:
    """
    Represents one discovered network port.
    """

    port: int
    protocol: str
    state: str
    service: str | None = None
    product: str | None = None
    version: str | None = None


@dataclass
class HostResult:
    """
    Represents one discovered host.
    """

    address: str
    hostname: str | None = None
    status: str = "unknown"
    ports: list[PortResult] = field(
        default_factory=list
    )


@dataclass
class NmapParseResult:
    """
    Structured result produced by the Nmap parser.
    """

    hosts: list[HostResult] = field(
        default_factory=list
    )

    @property
    def host_count(self) -> int:
        return len(self.hosts)

    @property
    def port_count(self) -> int:
        return sum(
            len(host.ports)
            for host in self.hosts
        )


class NmapParser:
    """
    Parser for standard Nmap text output.

    This parser intentionally handles common output
    rather than attempting to understand every possible
    Nmap output format.
    """

    HOST_PATTERN = re.compile(
        r"Nmap scan report for (.+)"
    )

    HOST_IP_PATTERN = re.compile(
        r"Nmap scan report for .*?\(([\d.:a-fA-F]+)\)"
    )

    HOST_STATUS_PATTERN = re.compile(
        r"Host is (up|down)"
    )

    PORT_PATTERN = re.compile(
        r"^(\d+)\/(\w+)\s+"
        r"(\w+)\s+"
        r"(\S+)"
        r"(?:\s+(.*))?$"
    )

    def parse(
        self,
        output: str,
    ) -> NmapParseResult:
        """
        Parse Nmap stdout.
        """

        result = NmapParseResult()

        current_host: HostResult | None = None

        for raw_line in output.splitlines():

            line = raw_line.strip()

            if not line:
                continue

            host_match = self.HOST_PATTERN.match(
                line
            )

            if host_match:

                host_text = host_match.group(1)

                ip_match = (
                    self.HOST_IP_PATTERN.match(
                        line
                    )
                )

                if ip_match:

                    address = (
                        ip_match.group(1)
                    )

                    hostname = (
                        host_text
                        .split(
                            "(",
                            1,
                        )[0]
                        .strip()
                    )

                else:

                    address = host_text
                    hostname = None

                current_host = HostResult(
                    address=address,
                    hostname=hostname,
                )

                result.hosts.append(
                    current_host
                )

                continue

            if current_host is None:
                continue

            status_match = (
                self.HOST_STATUS_PATTERN.search(
                    line
                )
            )

            if status_match:

                current_host.status = (
                    status_match.group(1)
                )

                continue

            if line.startswith(
                "PORT"
            ):

                continue

            port_match = self.PORT_PATTERN.match(
                line
            )

            if port_match:

                port = int(
                    port_match.group(1)
                )

                protocol = (
                    port_match.group(2)
                )

                state = (
                    port_match.group(3)
                )

                service = (
                    port_match.group(4)
                )

                details = (
                    port_match.group(5)
                )

                product = None
                version = None

                if details:

                    product = details.strip()

                current_host.ports.append(
                    PortResult(
                        port=port,
                        protocol=protocol,
                        state=state,
                        service=service,
                        product=product,
                        version=version,
                    )
                )

        return result