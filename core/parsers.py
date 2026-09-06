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

    extra: str | None = None


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
    Structured Nmap result.
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

    @property
    def open_port_count(self) -> int:
        return sum(
            1
            for host in self.hosts
            for port in host.ports
            if port.state == "open"
        )


class NmapParser:
    """
    Parser for common Nmap human-readable output.
    """

    HOST_PATTERN = re.compile(
        r"^Nmap scan report for (.+)$"
    )

    HOST_WITH_IP_PATTERN = re.compile(
        r"^(.+?)\s+\(([^)]+)\)$"
    )

    HOST_STATUS_PATTERN = re.compile(
        r"^Host is (up|down)"
    )

    PORT_PATTERN = re.compile(
        r"^(\d+)\/(\S+)\s+"
        r"(\S+)\s+"
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

            host = self._parse_host(line)

            if host is not None:

                current_host = host

                result.hosts.append(
                    current_host
                )

                continue

            if current_host is None:
                continue

            status = self._parse_host_status(
                line
            )

            if status is not None:

                current_host.status = status

                continue

            port = self._parse_port(
                line
            )

            if port is not None:

                current_host.ports.append(
                    port
                )

        return result

    def _parse_host(
        self,
        line: str,
    ) -> HostResult | None:
        """
        Parse:

            Nmap scan report for 192.168.1.10

        or:

            Nmap scan report for server.local
            (192.168.1.10)
        """

        match = self.HOST_PATTERN.match(
            line
        )

        if not match:
            return None

        value = match.group(1).strip()

        host_match = (
            self.HOST_WITH_IP_PATTERN.match(
                value
            )
        )

        if host_match:

            hostname = (
                host_match.group(1).strip()
            )

            address = (
                host_match.group(2).strip()
            )

            return HostResult(
                address=address,
                hostname=hostname,
            )

        return HostResult(
            address=value
        )

    def _parse_host_status(
        self,
        line: str,
    ) -> str | None:
        """
        Parse:

            Host is up
            Host is down
        """

        match = self.HOST_STATUS_PATTERN.match(
            line
        )

        if not match:
            return None

        return match.group(1)

    def _parse_port(
        self,
        line: str,
    ) -> PortResult | None:
        """
        Parse standard Nmap port lines.

        Example:

            22/tcp open ssh OpenSSH 9.9

        """

        match = self.PORT_PATTERN.match(
            line
        )

        if not match:
            return None

        port = int(
            match.group(1)
        )

        protocol = (
            match.group(2)
        )

        state = (
            match.group(3)
        )

        service = (
            match.group(4)
        )

        details = (
            match.group(5)
        )

        product = None
        version = None
        extra = None

        if details:

            product, version, extra = (
                self._parse_service_details(
                    details
                )
            )

        return PortResult(
            port=port,
            protocol=protocol,
            state=state,
            service=service,
            product=product,
            version=version,
            extra=extra,
        )

    def _parse_service_details(
        self,
        details: str,
    ) -> tuple[
        str | None,
        str | None,
        str | None,
    ]:
        """
        Attempt to separate product/version information.

        This is intentionally conservative because Nmap's
        service output is not guaranteed to follow one format.
        """

        details = details.strip()

        if not details:
            return None, None, None

        version_match = re.search(
            r"(?<!\d)"
            r"(\d+(?:\.\d+)+)"
            r"(?:[-_][A-Za-z0-9._-]+)?"
            r"(?!\d)",
            details,
        )

        if not version_match:

            return (
                details,
                None,
                None,
            )

        version = (
            version_match.group(1)
        )

        product = (
            details[:version_match.start()]
            .strip()
        )

        extra = (
            details[version_match.end():]
            .strip()
        )

        if not product:
            product = None

        if not extra:
            extra = None

        return (
            product,
            version,
            extra,
        )